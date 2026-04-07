from odoo import api,fields, models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    buyer_order_no = fields.Char(string="Buyer's Order No")
    buyer_order_date = fields.Date(string="Buyer's Order Date")
    proforma_invoice_date = fields.Date(string="Proforma Invoice Date")
