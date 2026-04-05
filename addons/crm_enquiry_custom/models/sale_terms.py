from odoo import fields, models


class SaleOrderTerm(models.Model):
    _name = "sale.order.term"
    _description = "Sales Order Term"
    _order = "id"

    sale_order_id = fields.Many2one("sale.order", string="Sales Order", required=True, ondelete="cascade", index=True)
    name = fields.Char(string="Lot Number", required=True, translate=True)
    term_description = fields.Text(string="Transformer Details", translate=True)
    qty_in_nos = fields.Integer(string="Quantity (Nos)")
    delivery_date = fields.Date(string="Delivery Date")



class SaleOrder(models.Model):
    _inherit = "sale.order"

    new_term_ids = fields.One2many("sale.order.term", "sale_order_id", string="Terms & Conditions", copy=True)
    delivery_order_note = fields.Html(string="Delivery Note")
