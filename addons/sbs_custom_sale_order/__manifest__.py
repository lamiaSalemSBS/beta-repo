{
    "name": "Beta Sales Order",
    "version": "18.0.1.0.0",
    "summary": "Adds a custom 'Beta Sales Order' fields for Sale Orders",
    "category": "Sales",
    "author": "Mohamed Hamed",
    "license": "LGPL-3",
    "depends": ["sale_management",'base','project', 'contacts', 'account'],
    "data": [

        "views/sale_order_view.xml",
    ],
    "installable": True,
    "application": False,
}
