# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class CrmEnquiryProject(models.Model):
    _name = 'crm.enquiry.project'
    _description = 'CRM Enquiry Project'
    _order = 'id'

    name = fields.Char(string='Project Reference', required=True)
    code = fields.Char(string='Code', help='Project code (can start with 0, e.g., 001, 010)')


class CrmEnquiryProjectType(models.Model):
    _name = 'crm.enquiry.project.type'
    _description = 'CRM Enquiry Project Type'
    _order = 'id'

    name = fields.Char(string='Project type', required=True)


class TechnicalParameter(models.Model):
    _name = 'technical.parameter'
    _description = 'Technical Parameter'
    _order = 'name'

    name = fields.Char(string='Description', required=True)
    unit = fields.Char(string='Unit')
    item_ids = fields.One2many('technical.parameter.item', 'parameter_id', string='Items')


class TechnicalParameterItem(models.Model):
    _name = 'technical.parameter.item'
    _description = 'Technical Parameter Item'
    _order = 'name'

    name = fields.Char(string='Item Value', required=True)
    parameter_id = fields.Many2one('technical.parameter', string='Parameter', required=True, ondelete='cascade')
