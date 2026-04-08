# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    print_layout = fields.Selection([('reference_po', 'Reference PO'), ('contract_agreement', 'Contract Agreement'),('normal_po', 'Normal PO')], string='PO Type', default='reference_po', required=True)
    responsible_eco_id = fields.Many2one('hr.employee', string='ECO.')
    responsible_dr_id = fields.Many2one('hr.employee', string='DR.')
    custom_notes_html = fields.Html(string='Custom Notes')


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    custom_description = fields.Text(string='Custom Description', compute='_compute_custom_description')
    qty_monthly_nos = fields.Float(string='Quantity Monthly (Nos)')
    weight_unit_kg = fields.Float(string='Weight/Unit (kg)')
    monthly_total_weight_kg = fields.Float(string='Monthly Total Weight (kg)', compute='_compute_custom_print_totals', store=True)
    monthly_amount = fields.Monetary(string='Monthly Amount', compute='_compute_custom_print_totals', store=True, currency_field='currency_id')
    month_total_weight_kg = fields.Float(string='Month Total Weight (kg)', compute='_compute_custom_print_totals', store=True)
    total_weight_kg = fields.Float(string='Total Weight (kg)', compute='_compute_custom_print_totals', store=True)
    delivery_date_text = fields.Char(string='Delivery Date')

    @api.depends('name', 'product_id')
    def _compute_custom_description(self):
        for line in self:
            if line.name and line.product_id:
                lines = line.name.split('\n')
                line.custom_description = '\n'.join(lines[1:]).strip() if len(lines) > 1 else ''
            else:
                line.custom_description = line.name or ''

    @api.depends('qty_monthly_nos', 'weight_unit_kg', 'product_qty', 'price_unit')
    def _compute_custom_print_totals(self):
        for line in self:
            line.monthly_total_weight_kg = line.qty_monthly_nos * line.weight_unit_kg
            line.monthly_amount = line.qty_monthly_nos * line.price_unit
            line.month_total_weight_kg = line.weight_unit_kg * line.product_qty
            line.total_weight_kg = line.product_qty * line.weight_unit_kg
