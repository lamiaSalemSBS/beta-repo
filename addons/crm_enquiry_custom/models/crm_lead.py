# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    enquiry_ids = fields.One2many('crm.enquiry.custom', 'lead_id', string='Enquiries')
    enquiry_count = fields.Integer(string='Enquiry Count', compute='_compute_enquiry_count')
    project_reference = fields.Many2one('crm.enquiry.project',string='Project Reference',required=True)
    project_type = fields.Many2one('crm.enquiry.project.type',string='Project Type',required=True)


    @api.depends('enquiry_ids')
    def _compute_enquiry_count(self):
        for record in self:
            record.enquiry_count = len(record.enquiry_ids)

    def action_create_enquiry(self):
        """Action button to create new enquiry"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Enquiry',
            'res_model': 'crm.enquiry.custom',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_lead_id': self.id,
                'default_partner_id': self.partner_id.id,
                'default_project_reference_id': self.project_reference.id if self.project_reference else False,
                'default_project_type_id': self.project_type.id if self.project_type else False,
            }
        }

    def action_view_enquiries(self):
        """Smart button to view enquiries"""
        action = self.env.ref('crm_enquiry_custom.action_crm_enquiry_custom').read()[0]
        action['domain'] = [('lead_id', '=', self.id)]
        action['context'] = {
            'default_lead_id': self.id,
            'default_partner_id': self.partner_id.id,
            'default_project_reference_id': self.project_reference.id if self.project_reference else False,
            'default_project_type_id': self.project_type.id if self.project_type else False,
        }
        return action
