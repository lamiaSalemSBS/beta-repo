# -*- coding: utf-8 -*-
##############################################################################
#
#    This module uses OpenERP, Open Source Management Solution Framework.
#    Copyright (C) 2017-Today Sitaram
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

{
    "name": "Beta Information module",
    "version": "18.0",
    "summary": "",
    "category": "Extra Addons",
    "description": """
    """,
    "author": "LS",
    "depends": ["base", "purchase", "purchase_requisition"],

    "data": [
        'report/report_purchase_order_view.xml',
        'report/report_purchase_order.xml',
        'view/purchase_requisition_form.xml'
    ],
    "license": "AGPL-3",
    "installable": True,
    "auto_install": False,
}
