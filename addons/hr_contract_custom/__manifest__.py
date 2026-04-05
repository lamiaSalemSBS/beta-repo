# -*- coding: utf-8 -*-
{
    'name': 'HR Contract Custom',
    'version': '18.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Add custom fields to HR Contract',
    'description': """
        This module adds custom fields to HR Contract:
        - Food Allowance
        - Total Salary (computed)
    """,
    'author': 'Your Company',
    'depends': ['hr_contract', 'hr', 'l10n_ae_hr_payroll'],
    'data': [
        'views/hr_contract_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
