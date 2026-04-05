# -*- coding: utf-8 -*-

from odoo import Command, _, api, fields, models


class CrmEnquiryLine(models.Model):
    _name = 'crm.enquiry.line'
    _description = 'CRM Enquiry Line'
    _order = 'sequence, id'

    enquiry_line_id = fields.Many2one('crm.enquiry.custom', string='Enquiry', required=True, ondelete='cascade')
    sequence = fields.Integer(string='Sequence', default=10)
    product_id = fields.Many2one('product.product', string='Product')
    name = fields.Char(string='Description', required=True)
    qty = fields.Float(string='Quantity', default=1.0)
    note = fields.Text(string='Note')
    detail_ids = fields.One2many('crm.enquiry.detail', 'line_subline_id', string='Details')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.name = self.product_id.name

    def action_show_details(self):
        """Open this line's details in a popup"""
        self.ensure_one()
        return {
            "name": _("Line Details"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "crm.enquiry.line",
            "res_id": self.id,
            "target": "new",
        }

    @api.model_create_multi
    def create(self, vals_list):
        lines = super(CrmEnquiryLine, self).create(vals_list)
        for line, vals in zip(lines, vals_list):
            if vals.get('detail_ids'):
                continue
            template = line.enquiry_line_id.detail_template_id
            if template:
                template_lines = template.line_ids.sorted(lambda l: (l.sequence, l.id))
                line.detail_ids = [Command.clear()] + [
                    Command.create({
                        'sequence': template_line.sequence,
                        'parameter_id': template_line.parameter_id.id,
                        'item_id': template_line.item_id.id,
                    })
                    for template_line in template_lines
                ]
        return lines


class CrmEnquiryDetail(models.Model):
    _name = 'crm.enquiry.detail'
    _description = 'CRM Enquiry Detail'
    _order = 'sequence, id'

    line_subline_id = fields.Many2one('crm.enquiry.line', string='Enquiry Line', required=True, ondelete='cascade')
    sequence = fields.Integer(string='Sequence', default=10)
    parameter_id = fields.Many2one('technical.parameter', string='Description', required=True)
    description = fields.Char(string='Description Text', related='parameter_id.name', store=True, readonly=True)
    unit = fields.Char(string='Unit', related='parameter_id.unit', store=True, readonly=True)
    item_id = fields.Many2one('technical.parameter.item', string='Item', domain="[('parameter_id', '=', parameter_id)]")

    @api.onchange('parameter_id')
    def _onchange_parameter_id(self):
        """Reset item when parameter changes"""
        if self.parameter_id:
            self.item_id = False
            # Return domain to filter items
            return {'domain': {'item_id': [('parameter_id', '=', self.parameter_id.id)]}}
        return {'domain': {'item_id': []}}
