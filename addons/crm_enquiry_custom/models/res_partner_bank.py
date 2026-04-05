# -*- coding: utf-8 -*-

from odoo import models, fields


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    iban = fields.Char(string='IBAN')
    cx_code = fields.Char(string='Swift Code')
    bank_address = fields.Char(string='Bank Address')
    acc_number = fields.Char(string='Account Number')

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    hs_code = fields.Char(string='HS Code')