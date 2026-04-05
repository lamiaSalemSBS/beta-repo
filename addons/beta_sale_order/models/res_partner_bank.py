# -*- coding: utf-8 -*-
from odoo import fields, models

class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    x_iban = fields.Char(string='IBAN', help='International Bank Account Number')
    x_swift_code = fields.Char(string='Swift Code', help='BIC / SWIFT code')
