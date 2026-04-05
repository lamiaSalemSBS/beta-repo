# -*- coding: utf-8 -*-
{
    'name': 'Custom Print Reports',
    'version': '18.0.1.0.0',
    'category': 'Reporting',
    'summary': 'Custom print reports for Sale, Account, and Purchase',
    'description': """
        Custom Print Reports
        ====================
        This module provides custom print reports for:
        * Sale Orders
        * Invoices (Account)
        * Purchase Orders
    """,
    'author': 'SBS',
    'website': '',
    'depends': [
        'base',
        'sale_management',
        'account',
        'purchase',
        'web',
        'hr',
    ],
    'data': [
        'data/paper_format.xml',
        'views/sale_order_view.xml',
        'views/purchase_order_view.xml',
        'reports/report_action.xml',
        'reports/sale_report_template.xml',
        'reports/sale_offer_template.xml',
        'reports/account_report_template.xml',
        'reports/purchase_report_template.xml',
        'reports/purchase_report_contract_template.xml',

        'reports/report_commercial_invoice_template.xml',
        'reports/report_packing_list_template.xml',
        'reports/report_pro_forma_sale_template.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
