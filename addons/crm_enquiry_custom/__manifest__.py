# -*- coding: utf-8 -*-
{
    'name': 'CRM Enquiry Custom',
    'version': '18.0.1.4.0',
    'category': 'CRM',
    'summary': 'Custom Enquiry Management in CRM',
    'author': 'Abd Elhamed Saad',
    'website': 'https://www.linkedin.com/in/abd-elhamed-saad/',
    'description': """
        CRM Enquiry Management Module
        ==============================
        * Create enquiries from CRM leads
        * Manage enquiry lines and details
        * Generate enquiry reports
        * Wizard for enquiry processing
    """,
    'depends': ['crm', 'product', 'sale', 'sale_crm', 'hr', 'mrp', 'sale_stock'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/technical_parameter_views.xml',
        'views/detail_template_views.xml',
        'views/crm_enquiry_custom_views.xml',
        'views/crm_lead_views.xml',
        'views/sale_order_views.xml',
        'views/res_partner_bank_views.xml',
        'views/sale_terms_view.xml',
        'wizard/enquiry_wizard_views.xml',
        'report/enquiry_report.xml',
        'report/enquiry_report_template.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
