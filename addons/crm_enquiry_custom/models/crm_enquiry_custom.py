# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import Command, api, fields, models


class CrmEnquiryCustom(models.Model):
    _name = 'crm.enquiry.custom'
    _description = 'CRM Enquiry Custom'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Enquiry Reference', required=True, copy=False, readonly=True, default='New')
    original_name = fields.Char(string='Original Reference', copy=True, readonly=True,
                                help='Original enquiry reference for tracking revisions')
    lead_id = fields.Many2one('crm.lead', string='CRM Lead', required=True, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True, tracking=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company, required=True,
                                 tracking=True)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id,
                                  required=True, tracking=True)
    project_reference_id = fields.Many2one('crm.enquiry.project', string='Project Reference', required=True,
                                           tracking=True)
    project_reference = fields.Char(string='Project Reference Text', related='project_reference_id.name', store=True,
                                    readonly=True)
    project_reference_code = fields.Char(string='Project Code', related='project_reference_id.code', store=True,
                                         readonly=True)
    project_type_id = fields.Many2one('crm.enquiry.project.type', string='Project Type', required=True, tracking=True)
    project_type = fields.Char(string='Project Type Text', related='project_type_id.name', store=True, readonly=True)
    date = fields.Date(string='Date', default=fields.Date.context_today, required=True, tracking=True)
    revision = fields.Integer(string='Revision', default=0, tracking=True, copy=False)
    customer_reference = fields.Char(string='Customer Reference', tracking=True)
    notes = fields.Html(string='Notes')
    detail_template_id = fields.Many2one('crm.enquiry.detail.template', string='Details Template', tracking=True, )
    line_ids = fields.One2many('crm.enquiry.line', 'enquiry_line_id', string='Enquiry Lines')
    state = fields.Selection(
        [('draft', 'Draft'), ('confirmed', 'Confirmed'), ('done', 'Done'), ('cancel', 'Cancelled')], string='Status',
        default='draft', tracking=True)

    # Sale Order fields
    sale_order_ids = fields.One2many('sale.order', 'enquiry_id', string='Sale Orders')
    sale_order_count = fields.Integer(string='Sale Order Count', compute='_compute_sale_order_count')
    consignee = fields.Many2one('res.partner', string='Consignee')
    notify = fields.Many2one('res.partner', string='Notify')

    def _compute_sale_order_date(self):
        for enquiry in self:
            enquiry.sale_order_date = enquiry.sale_order_ids.date_order if enquiry.sale_order_ids else False

    def _prepare_detail_line_commands(self):
        self.ensure_one()
        template_lines = self.detail_template_id.line_ids.sorted(lambda l: (l.sequence, l.id))
        return [
            Command.create({
                'sequence': template_line.sequence,
                'parameter_id': template_line.parameter_id.id,
                'item_id': template_line.item_id.id,
            })
            for template_line in template_lines
        ]

    def _apply_details_template_replace(self):
        for enquiry in self.filtered('detail_template_id'):
            detail_commands = enquiry._prepare_detail_line_commands()
            for line in enquiry.line_ids:
                line.detail_ids = [Command.clear(), *detail_commands]

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            # Get date for year and month
            enquiry_date = vals.get('date', fields.Date.context_today(self))
            if isinstance(enquiry_date, str):
                enquiry_date = datetime.strptime(enquiry_date, '%Y-%m-%d').date()

            year_short = str(enquiry_date.year)[2:]  # Last 2 digits of year
            month = f"{enquiry_date.month:02d}"  # Month with leading zero

            # Get project reference code
            project_ref_id = vals.get('project_reference_id')
            project_ref = self.env['crm.enquiry.project'].browse(project_ref_id)
            project_code = project_ref.code or False
            # Get sequence prefix
            sequence = self.env['ir.sequence'].search([('code', '=', 'crm.enquiry.custom')], limit=1)
            prefix = sequence.prefix if sequence else 'BETA-ENQ'
            padding = int(sequence.padding) if sequence and sequence.padding else 4
            # ------------------------------------------------
            # Build prefix dynamically (project code optional)
            # ------------------------------------------------
            sequence_parts = [prefix, year_short, month]
            if project_code:
                sequence_parts.append(project_code)

            year_month_project_prefix = "-".join(sequence_parts)

            # Find last enquiry with same prefix
            all_enquiries = self.search([
                ('name', 'like', f"{year_month_project_prefix}-%"),
                ('name', '!=', 'New')
            ], order='name desc')

            next_number = 1
            for enq in all_enquiries:
                if enq.name.startswith(year_month_project_prefix + '-'):
                    remaining = enq.name[len(year_month_project_prefix) + 1:]
                    parts = remaining.split('-')

                    # Base enquiry only (exclude revisions)
                    if len(parts) == 1:
                        try:
                            current_number = int(parts[0])
                            if current_number >= next_number:
                                next_number = current_number + 1
                        except ValueError:
                            continue

            # Final name
            new_name = f"{year_month_project_prefix}-{next_number:0{padding}d}"
            vals['name'] = new_name

            if 'original_name' not in vals:
                vals['original_name'] = new_name

        enquiry = super(CrmEnquiryCustom, self).create(vals)
        if vals.get('detail_template_id'):
            enquiry._apply_details_template_replace()
        return enquiry

    def write(self, vals):
        template_changed = 'detail_template_id' in vals
        result = super(CrmEnquiryCustom, self).write(vals)
        if template_changed:
            self._apply_details_template_replace()
        return result

    def copy(self, default=None):
        """Create a copy of the enquiry with revision number"""
        self.ensure_one()
        default = dict(default or {})

        # Get the base reference (original enquiry number)
        base_sequence = self.original_name if self.original_name else self.name

        # Find the highest revision for this base sequence
        all_revisions = self.search([
            '|',
            ('original_name', '=', base_sequence),
            ('name', '=', base_sequence)
        ], order='revision desc', limit=1)

        # Calculate next revision number
        if all_revisions:
            next_revision = all_revisions.revision + 1
        else:
            next_revision = 1

        # Format: BETA-ENQ-YY-MM-XXX-NNNN-RR (where RR is revision)
        new_name = f"{base_sequence}-{next_revision:02d}"

        default['name'] = new_name
        default['original_name'] = base_sequence
        default['revision'] = next_revision
        default['state'] = 'draft'  # Reset to draft when copying

        return super(CrmEnquiryCustom, self).copy(default)

    @api.onchange('lead_id')
    def _onchange_lead_id(self):
        if self.lead_id:
            self.partner_id = self.lead_id.partner_id
            self.project_reference_id = self.lead_id.project_reference.id
            self.project_type_id = self.lead_id.project_type.id

    @api.onchange('detail_template_id')
    def _onchange_detail_template_id(self):
        if self.detail_template_id:
            self._apply_details_template_replace()

    def action_confirm(self):
        self.state = 'confirmed'

    def action_done(self):
        self.state = 'done'

    def action_cancel(self):
        self.state = 'cancel'

    def action_draft(self):
        self.state = 'draft'

    def action_create_revision(self):
        """Create a new revision of the enquiry"""
        self.ensure_one()
        old_revision = self.revision
        self.revision = old_revision + 1

    @api.depends('sale_order_ids')
    def _compute_sale_order_count(self):
        for record in self:
            record.sale_order_count = len(record.sale_order_ids)

    def action_create_quotation_enquiry(self):
        """Create quotation from enquiry"""
        order_lines = []
        for line in self.line_ids:
            order_lines.append((0, 0, {
                'product_id': line.product_id.id,
                'name': line.name,
                'product_uom_qty': line.qty,
                'note': line.note,
            }))

        # Create sale order
        sale_order = self.env['sale.order'].create({
            'partner_id': self.partner_id.id,
            'enquiry_id': self.id,
            'project_type_id': self.project_type_id.id,
            'consignee': self.consignee.id,
            'notify': self.notify.id,
            'opportunity_id': self.lead_id.id,
            'client_order_ref': self.customer_reference,
            'order_line': order_lines,
            'project_reference_id': self.project_reference_id.id,
        })

        return {
            'type': 'ir.actions.act_window',
            'name': 'Quotation',
            'res_model': 'sale.order',
            'res_id': sale_order.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_view_sale_orders(self):
        """Smart button to view sale orders"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sale Orders',
            'res_model': 'sale.order',
            'view_mode': 'list,form',
            'domain': [('enquiry_id', '=', self.id)],
            'context': {
                'default_enquiry_id': self.id,
                'default_partner_id': self.partner_id.id,
                'default_consignee': self.consignee.id,
                'default_notify': self.notify.id,
            },
        }
