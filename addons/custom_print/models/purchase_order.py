# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    print_layout = fields.Selection([('normal_po', 'Normal PO'),('reference_po', 'Reference PO'), ('contract_agreement', 'Contract Agreement')], string='PO Type', default='normal_po', required=True)
    responsible_eco_id = fields.Many2one('hr.employee', string='ECO.')
    responsible_dr_id = fields.Many2one('hr.employee', string='DR.')
    custom_notes_html = fields.Html(string='Custom Notes')


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    custom_description = fields.Text(string='Custom Description', compute='_compute_custom_description')
    qty_monthly_nos = fields.Float(string='Quantity Monthly (Nos)')
    ref_number_of_months = fields.Float(string='Number of Months')
    weight_unit_kg = fields.Float(string='Weight/Unit (kg)')
    ref_weight_unit_kg = fields.Float(string='Weight/Unit (kg)')
    monthly_total_weight_kg = fields.Float(string='Monthly Total Weight (kg)', compute='_compute_custom_print_totals', store=True)
    monthly_amount = fields.Monetary(string='Monthly Amount', compute='_compute_custom_print_totals', store=True, currency_field='currency_id')
    month_total_weight_kg = fields.Float(string='Month Total Weight (kg)', compute='_compute_custom_print_totals', store=True)
    total_weight_kg = fields.Float(string='Total Weight (kg)', compute='_compute_custom_print_totals', store=True)
    ref_monthly_total_weight_kg = fields.Float(string='Monthly Total Weight (kg)', compute='_ref_compute_custom_print_totals',
                                           store=True)
    ref_monthly_amount = fields.Monetary(string='Monthly Amount', compute='_ref_compute_custom_print_totals', store=True,
                                     currency_field='currency_id')
    ref_month_total_weight_kg = fields.Float(string='Month Total Weight (kg)', compute='_ref_compute_custom_print_totals',
                                         store=True)
    ref_total_weight_kg = fields.Float(string='Total Weight (kg)', compute='_ref_compute_custom_print_totals', store=True)
    ref_total_months_qty = fields.Float(string='Total qty ', compute='_ref_compute_custom_print_totals', store=True)
    ref_total_months_amount = fields.Float(string='Total Amount ', compute='_ref_compute_custom_print_totals', store=True)

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

    @api.depends('qty_monthly_nos','ref_weight_unit_kg',
                 'product_qty', 'price_unit',
                 'ref_number_of_months','ref_monthly_total_weight_kg',
                 'ref_total_months_qty')
    def _ref_compute_custom_print_totals(self):
        for line in self:
            line.ref_monthly_total_weight_kg = line.qty_monthly_nos * line.ref_weight_unit_kg
            line.ref_monthly_amount = line.ref_monthly_total_weight_kg * line.price_unit
            line.ref_month_total_weight_kg = line.ref_weight_unit_kg * line.qty_monthly_nos
            line.ref_total_months_qty = line.qty_monthly_nos * line.ref_number_of_months
            line.ref_total_weight_kg = line.ref_total_months_qty * line.ref_weight_unit_kg
            line.ref_total_months_amount = line.ref_monthly_amount * line.ref_number_of_months

    @api.depends(
        'product_qty',
        'price_unit',
        'taxes_id',
        'total_weight_kg',
        'order_id.print_layout'
    )
    def _compute_amount(self):
        for line in self:

            if line.order_id.print_layout == 'reference_po':
                subtotal = line.total_weight_kg * line.price_unit

                taxes = line.taxes_id.compute_all(
                    line.price_unit,
                    currency=line.order_id.currency_id,
                    quantity=line.total_weight_kg,
                    product=line.product_id,
                    partner=line.order_id.partner_id
                )

                line.update({
                    'price_subtotal': subtotal,
                    'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                    'price_total': subtotal + sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                })

            else:
                super(PurchaseOrderLine, line)._compute_amount()