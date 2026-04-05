from odoo import models, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    show_validate = fields.Boolean(default=False,string="Show Validate")


    def check_quality(self):
        res = super().check_quality()
        for rec in self:
            rec.show_validate = True
        return res