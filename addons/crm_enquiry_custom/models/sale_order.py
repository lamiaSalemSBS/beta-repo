# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    enquiry_id = fields.Many2one('crm.enquiry.custom', string='Enquiry Reference', tracking=True)
    project_type_id = fields.Many2one('crm.enquiry.project.type', string='Project Type', tracking=True)
    consignee = fields.Many2one('res.partner', string='Consignee', tracking=True)
    notify = fields.Many2one('res.partner', string='Notify', tracking=True)

    # Office Memo - Employee fields
    engineering_id = fields.Many2one('hr.employee', string='Engineering', tracking=True)
    planning_purchase_id = fields.Many2one('hr.employee', string='Planning & Purchase', tracking=True)
    accounts_id = fields.Many2one('hr.employee', string='Accounts', tracking=True)
    operations_id = fields.Many2one('hr.employee', string='Operations', tracking=True)
    testing_id = fields.Many2one('hr.employee', string='Testing', tracking=True)
    store_id = fields.Many2one('hr.employee', string='Store', tracking=True)

    # Bank details from partner
    partner_bank_id = fields.Many2one('res.partner.bank', string='Bank Account', tracking=True)

    # Related bank fields
    bank_iban = fields.Char(string='IBAN', related='partner_bank_id.iban', readonly=True)
    bank_currency = fields.Many2one('res.currency',string='Currency', related='partner_bank_id.currency_id', readonly=True)
    bank_cx_code = fields.Char(string='Swift Code', related='partner_bank_id.cx_code', readonly=True)
    bank_address = fields.Char(string='Bank Address', related='partner_bank_id.bank_address', readonly=True)
    bank_account_number = fields.Char(string='Account Number', related='partner_bank_id.acc_number', readonly=True)
    revision = fields.Integer(string='Revision', default=0)
    project_reference_id = fields.Many2one('crm.enquiry.project', string='Project Reference', required=True,
                                           tracking=True)
    form_invoice_seq = fields.Char(string='Proform Invoice Sequence', readonly=True)

    payment_schedule = fields.Html(string="Payment Schedule")

    @api.model
    def create(self, vals):
        """Override create to generate Beta-Offer sequence for new orders"""
        # Generate Beta-Offer sequence directly in 'name' field
        if vals.get('name', '/') == '/' or 'name' not in vals:
            # Get date for year and month
            order_date = vals.get('date_order', fields.Datetime.now())
            if isinstance(order_date, str):
                order_date = datetime.strptime(order_date, '%Y-%m-%d %H:%M:%S')

            year_short = str(order_date.year)[2:]  # Last 2 digits (25, 26, etc.)
            month = f"{order_date.month:02d}"  # Month with leading zero (01-12)

            # Get sequence
            sequence = self.env['ir.sequence'].next_by_code('sale.order.beta.offer')
            if sequence:
                # Extract the number from sequence (remove prefix if it exists)
                # The sequence returns something like "Beta-Offer000001"
                # We need to rebuild it as "Beta-Offer-YY-MM-NNNNNN"
                seq_number = sequence.replace('Beta-Offer', '')
                vals['name'] = f"Beta-Offer-{year_short}-{month}-{seq_number}"
        return super(SaleOrder, self).create(vals)

    # def action_confirm(self):
    #     """Override action_confirm to generate SO sequence when confirming"""
    #     for order in self:
    #         # Check if current name is Beta-Offer format (starts with "Beta-Offer")
    #         if order.name and order.name.startswith('Beta-Offer'):
    #             # Replace Beta-Offer sequence with standard SO sequence
    #             order.name = self.env['ir.sequence'].next_by_code('sale.order') or '/'
    #
    #         if order.name:
    #             seq_number = order.name.replace('Beta-SO', '')
    #             order.form_invoice_seq = f"Beta-PI{seq_number}"
    #
    #     return super(SaleOrder, self).action_confirm()

    def action_create_revision(self):
        """Create a new revision of the enquiry"""
        self.ensure_one()
        old_revision = self.revision
        self.revision = old_revision + 1


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    note = fields.Text(string='Note')
