# -*- coding: utf-8 -*-

from odoo import fields, models


class CrmEnquiryDetailTemplate(models.Model):
    _name = "crm.enquiry.detail.template"
    _description = "CRM Enquiry Detail Template"
    _order = "name, id"

    name = fields.Char(string="Template Name", required=True)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one("res.company", string="Company", default=lambda self: self.env.company)
    line_ids = fields.One2many("crm.enquiry.detail.template.line", "template_id", string="Template Lines", )


class CrmEnquiryDetailTemplateLine(models.Model):
    _name = "crm.enquiry.detail.template.line"
    _description = "CRM Enquiry Detail Template Line"
    _order = "sequence, id"

    template_id = fields.Many2one("crm.enquiry.detail.template", string="Template", required=True, ondelete="cascade", )
    sequence = fields.Integer(string="Sequence", default=10)
    parameter_id = fields.Many2one("technical.parameter", string="Description", required=True)
    description = fields.Char(string="Description Text", related="parameter_id.name", store=True, readonly=True, )
    unit = fields.Char(string="Unit", related="parameter_id.unit", store=True, readonly=True, )
    item_id = fields.Many2one("technical.parameter.item", string="Item",
                              domain="[('parameter_id', '=', parameter_id)]", )
