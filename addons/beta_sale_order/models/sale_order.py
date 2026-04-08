from odoo import api,fields, models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    x_enquiry_reference = fields.Char(
        string="Enquiry Reference",
        help="Customer enquiry / reference for this quotation or order.",
        copy=False,
    )

    x_attention_id = fields.Many2one(
        "res.partner",
        string="Kind of Attention",
        help="Person to address (Attn:). Choose a contact belonging to the selected customer.",
        ondelete="set null",
        domain="[('type', 'in', ['contact','other'])]",  # coarse filter; view adds tighter domain
    )

    x_project_id = fields.Many2one(
        "project.project",
        string="Project Reference",
        help="Link this quotation/order to a Project.",
        ondelete="set null",
    )

    x_offer_notes = fields.Text(string='Notes (one per line)')

    buyer_order_no = fields.Text(string="Buyer's Order No")
    buyer_order_date = fields.Date(string="Buyer's Order Date")
    proforma_invoice_date = fields.Date(string="Proforma Invoice Date")

    @api.onchange("partner_id")
    def _onchange_partner_id_reset_attention(self):
        """When customer changes, clear Attention if it no longer belongs to that customer."""
        if self.x_attention_id and self.partner_id and \
           self.x_attention_id.commercial_partner_id != self.partner_id.commercial_partner_id:
            self.x_attention_id = False