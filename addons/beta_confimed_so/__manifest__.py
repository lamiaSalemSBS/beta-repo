{
    'name': 'Quotation to Sale Order Management',
    "version": "18.0",
    'summary': 'Manage Quotations and Confirmed Sale Orders separately',
    'category': 'Sales',
    'author': 'Your Company',
    'website': 'https://yourcompany.com',
    'depends': ['sale','crm_enquiry_custom'],
    'data': [
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}