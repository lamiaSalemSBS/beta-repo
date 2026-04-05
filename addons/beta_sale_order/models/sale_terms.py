from odoo import fields, models

class SaleOrderTerm(models.Model):
    _name = "sale.order.term"
    _description = "Sales Order Term"
    _order = "id"

    sale_order_id = fields.Many2one(
        "sale.order", string="Sales Order",
        required=True, ondelete="cascade", index=True
    )
    name = fields.Char(string="Title", required=True, translate=True)
    term_description = fields.Text(string="Description", translate=True)

class SaleOrder(models.Model):
    _inherit = "sale.order"

    x_term_ids = fields.One2many(
        "sale.order.term", "sale_order_id",
        string="Terms & Conditions", copy=True
    )
