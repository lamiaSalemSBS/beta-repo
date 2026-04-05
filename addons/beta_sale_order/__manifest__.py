{
    "name": "Beta Sales Order",
    "version": "18.0.1.0.0",
    "summary": "Adds a custom 'Beta Sales Order' print for Sale Orders",
    "category": "Sales",
    "author": "You",
    "license": "LGPL-3",
    "depends": ["sale_management",'base','project', 'contacts', 'account'],
    "data": [
        'security/ir.model.access.csv',
        "views/sale_report_action.xml",
        "report/sale_beta_templates.xml",
        "views/sale_order_view.xml",
        "views/sale_attention_view.xml",  # (this new file)
        "views/sale_project_ref_view.xml" , # (Project Reference)
        'views/res_partner_bank_view.xml',
        # "views/sale_order_notes_view.xml",
        'views/sale_terms_view.xml',
    ],
    "installable": True,
    "application": False,
}
