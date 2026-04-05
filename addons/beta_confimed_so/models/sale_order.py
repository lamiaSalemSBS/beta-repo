from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    parent_quotation_id = fields.Many2one(
        'sale.order',
        string='Parent Quotation',
        copy=False,
        index=True,
        ondelete='set null'
    )

    confirmed_so_ids = fields.One2many(
        'sale.order',
        'parent_quotation_id',
        string='Confirmed Sale Orders',
        copy=False
    )

    # Add computed field for count
    confirmed_so_count = fields.Integer(
        string='Confirmed SOs Count',
        compute='_compute_confirmed_so_count',
        store=True
    )
    @api.depends('confirmed_so_ids', 'confirmed_so_ids.state')
    def _compute_has_active_so(self):
        for order in self:
            # Check if there's any sale order in 'sale' state
            active_sos = order.confirmed_so_ids.filtered(lambda so: so.state == 'sale')
            order.has_active_so = bool(active_sos)
    has_active_so = fields.Boolean(
        string='Has Active SO',
        compute='_compute_has_active_so',
        store=True
    )
    is_confirmed_from_qt = fields.Boolean(
        string='Confirmed from Quotation',
        compute='_compute_is_confirmed_from_qt',
        store=True
    )

    @api.depends('parent_quotation_id')
    def _compute_is_confirmed_from_qt(self):
        for order in self:
            order.is_confirmed_from_qt = bool(order.parent_quotation_id)

    @api.depends('confirmed_so_ids')
    def _compute_confirmed_so_count(self):
        for order in self:
            order.confirmed_so_count = len(order.confirmed_so_ids)

    def action_confirm(self):

        self.ensure_one()

        if self.is_confirmed_from_qt:
            return super().action_confirm()

        confirmed_sale_orders = self.confirmed_so_ids.filtered(lambda so: so.state == 'sale')

        if self.state in ['draft', 'sent'] and not confirmed_sale_orders:

            # standard SO sequence
            so_seq = self.env['ir.sequence'].next_by_code('sale.order')

            # build PI sequence from same number
            seq_number = so_seq
            if seq_number.startswith('Beta-SO'):
                seq_number = seq_number.replace('Beta-SO', '').strip('-')

            pi_seq = f"Beta-PI-{seq_number}"

            new_so_vals = {
                'parent_quotation_id': self.id,
                'state': 'sale',
                'date_order': fields.Datetime.now(),

                # SO number
                'name': so_seq,

                # PI number
                'form_invoice_seq': pi_seq,

                'origin': self.name,
                'partner_id': self.partner_id.id,
                'partner_invoice_id': self.partner_invoice_id.id,
                'partner_shipping_id': self.partner_shipping_id.id,
                'pricelist_id': self.pricelist_id.id,
                'payment_term_id': self.payment_term_id.id,
                'fiscal_position_id': self.fiscal_position_id.id,
                'company_id': self.company_id.id,
                'user_id': self.user_id.id,
                'team_id': self.team_id.id,
                'client_order_ref': self.client_order_ref,
                'require_signature': self.require_signature,
                'require_payment': self.require_payment,
                'commitment_date': self.commitment_date,
                'project_reference_id': self.project_reference_id.id,
            }

            new_so = self.create(new_so_vals)

            for line in self.order_line:
                line.copy({
                    'order_id': new_so.id,
                    'product_id': line.product_id.id,
                    'name': line.name,
                    'product_uom_qty': line.product_uom_qty,
                    'product_uom': line.product_uom.id,
                    'price_unit': line.price_unit,
                    'tax_id': [(6, 0, line.tax_id.ids)],
                    'discount': line.discount,
                })

            return {
                'type': 'ir.actions.act_window',
                'name': _('Sale Order'),
                'res_model': 'sale.order',
                'res_id': new_so.id,
                'views': [(False, 'form')],
                'context': {'form_view_initial_mode': 'edit'},
                'target': 'current',
            }

        return super().action_confirm()

    def action_cancel(self):
        """Override cancel action to handle reset to draft from confirmed SO"""
        self.ensure_one()

        # If this is a confirmed SO from QT
        if self.parent_quotation_id:
            parent_qt = self.parent_quotation_id

            # Cancel related records
            self._cancel_related_records(self)

            # Instead of archiving, change state to cancel
            self.write({'state': 'cancel'})

            # Return action to view the parent QT (which remains draft)
            return {
                'type': 'ir.actions.act_window',
                'name': _('Quotation'),
                'res_model': 'sale.order',
                'res_id': parent_qt.id,
                'views': [(False, 'form')],
                'context': self.env.context,
                'target': 'current',
            }

        # For normal sale orders or QTs without parent
        return super().action_cancel()

    def _cancel_related_records(self, so):
        """Cancel all related records (invoices, pickings, etc.)"""
        # Cancel related invoices
        if so.invoice_ids:
            for invoice in so.invoice_ids:
                if invoice.state == 'draft':
                    invoice.button_cancel()

        # Cancel related pickings
        if so.picking_ids:
            for picking in so.picking_ids:
                if picking.state not in ['done', 'cancel']:
                    picking.action_cancel()

    def action_view_confirmed_sos(self):
        """Action to view confirmed SOs from this QT"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Sale Orders from %s') % self.name,
            'res_model': 'sale.order',
            'view_mode': 'list,form',
            'domain': [('parent_quotation_id', '=', self.id)],
            'context': {
                'create': False,
            },
            'target': 'current',
        }

    def reset_quotation(self):
        """Reset QT to draft and cancel related confirmed SOs"""
        for order in self:
            # Cancel all related confirmed SOs that are in 'sale' state
            for confirmed_so in order.confirmed_so_ids.filtered(lambda so: so.state == 'sale'):
                confirmed_so.action_cancel()

            # Show notification
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Quotation Reset'),
                    'message': _('All related Sale Orders have been cancelled.'),
                    'type': 'success',
                    'sticky': False,
                }
            }

    @api.model
    def create(self, vals):
        """Set proper name for confirmed SOs from QT"""
        if vals.get('parent_quotation_id') and not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code('sale.order') or '/'
        return super().create(vals)

    def copy(self, default=None):
        """Override copy to handle copying of QT"""
        if default is None:
            default = {}

        if self.is_confirmed_from_qt:
            default['parent_quotation_id'] = False
            default['is_confirmed_from_qt'] = False

        return super().copy(default)
