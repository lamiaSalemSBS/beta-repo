# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class EnquiryWizard(models.TransientModel):
    _name = 'enquiry.wizard'
    _description = 'Enquiry Wizard'

