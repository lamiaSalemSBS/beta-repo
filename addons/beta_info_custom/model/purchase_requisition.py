# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models
from dateutil.relativedelta import relativedelta


class PurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'

    payment_term_id = fields.Many2one(
        comodel_name='account.payment.term',
        string="Payment Terms",
        store=True, readonly=False, precompute=True, check_company=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")

    delivery_terms = fields.Char(string="Delivery Terms", )

    contract_period = fields.Char(string="Contract Period", compute="_compute_contract_period")

    def _compute_contract_period(self):
        for rec in self:
            rec.contract_period = ''
            if rec.date_start and rec.date_end:
                delta = relativedelta(rec.date_end, rec.date_start)
                # If less than 1 month, show in days
                if delta.years == 0 and delta.months == 0:
                    days = (rec.date_end - rec.date_start).days
                    rec.contract_period = f"{days} Days"
                else:
                    total_months = delta.years * 12 + delta.months
                    rec.contract_period = f"{total_months} Months"
class PurchaseRequisitionLine(models.Model):
    _inherit = "purchase.requisition.line"

    weight_kg_unit = fields.Float(string="Weight (kg) Unit")
    contract_period = fields.Char(string="Contract Period")
    total_weight_kg_monthly = fields.Float(string="Total Weight (Kg) Monthly")
    unit_price_per_kg = fields.Float(string="Unit Price / KG")
    monthly_amount = fields.Float(string="Monthly Amount")
    monthly_contract_qty = fields.Float(string="Monthly Contract Qty")
    monthly_contract_total_weight = fields.Float(string="Monthly Contract Total Weight")
    monthly_contract_amount = fields.Float(string="Monthly Contract Amount")
    delivery_terms = fields.Text(string="Delivery Terms")