# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AccountMoveLineDetailsWizard(models.TransientModel):
    _name = 'account.move.line.details.wizard'
    _description = 'Account Move Line Details Wizard'

    move_line_id = fields.Many2one('account.move.line', string='Move Line', required=True)
    qty = fields.Float(string="Quantity", compute='_compute_qty', readonly=False, store=True)
    length = fields.Float(string="Length MM")
    width = fields.Float(string="Width MM")
    height = fields.Float(string="Height MM")
    net_weight = fields.Float(string="Net Weight (Kg)")
    gross_weight = fields.Float(string="Gross Weight", compute='_compute_gross_weight', readonly=False, store=True)
    total_gross_weight_with_packaging = fields.Float(string="Total Gross Weight With Packaging", compute='_compute_total_gross_weight', readonly=False, store=True)

    @api.depends('move_line_id')
    def _compute_qty(self):
        for rec in self:
            if rec.move_line_id:
                rec.qty = rec.move_line_id.quantity
            else:
                rec.qty = 0.0

    @api.depends('net_weight')
    def _compute_gross_weight(self):
        for rec in self:
            rec.gross_weight = rec.net_weight + 50 if rec.net_weight else 0.0

    @api.depends('qty', 'gross_weight')
    def _compute_total_gross_weight(self):
        for rec in self:
            rec.total_gross_weight_with_packaging = rec.qty * rec.gross_weight

    def action_save(self):
        self.ensure_one()
        self.move_line_id.write({
            'line_qty': self.qty,
            'line_length': self.length,
            'line_width': self.width,
            'line_height': self.height,
            'line_net_weight': self.net_weight,
            'line_gross_weight': self.gross_weight,
            'line_total_gross_weight_with_packaging': self.total_gross_weight_with_packaging,
        })
        return {'type': 'ir.actions.act_window_close'}
