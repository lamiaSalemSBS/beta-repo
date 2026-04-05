# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HrContractCustom(models.Model):
    _inherit = 'hr.contract'

    food = fields.Float(string='Food Allowance', help='Monthly food allowance', tracking=True)

    salary = fields.Float(string='Total Salary', compute='_compute_salary', store=True, tracking=True)

    @api.onchange('wage', 'l10n_ae_housing_allowance', 'l10n_ae_transportation_allowance', 'l10n_ae_other_allowances')
    def _compute_salary(self):
        for contract in self:
            contract.salary = contract.wage + contract.l10n_ae_housing_allowance + contract.l10n_ae_transportation_allowance + contract.l10n_ae_other_allowances
