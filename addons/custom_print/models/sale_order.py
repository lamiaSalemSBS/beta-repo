# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    kind_attention_id = fields.Many2one('hr.employee', string='Kind Attention', )
    note_text = fields.Html(string='Note', help='Additional notes similar to terms and conditions')

    kind_child_attention_id = fields.Many2one('res.partner', string='Kind Attention',
                                              domain="[('parent_id', '=', partner_id)]", )
    place_of_loading = fields.Char(string='Place of Loading')
    manager_id = fields.Many2one('hr.employee', string='Manager',)


    @api.onchange('partner_id')
    def _onchange_partner_id_kind_attention(self):
        for order in self:
            order.kind_child_attention_id = False
            if order.partner_id:
                child = self.env['res.partner'].search(
                    [('parent_id', '=', order.partner_id.id)],
                    limit=1,
                    order='id asc'
                )
                order.kind_child_attention_id = child
