# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Sales Terms & Conditions",

    "author": "Softhealer Technologies",

    "license": "OPL-1",

    "website": "https://www.softhealer.com",

    "support": "support@softhealer.com",

    "version": "15.0.4",

    "category": "Sales",

    "summary": "Show Sales Terms And Condition App, Create Quotation Terms And Condition Module, Set SO Terms And Condition, Sale Order Terms & Condition, Quote Terms & Condition Odoo",

    "description": """Each and every seller have to declare its company policy that provides terms & condition. This module is used to display terms and conditions when any quotation creates. You can create terms and conditions easily using the HTML input tool. You can print terms & conditions in the quotation and sale order report.Sales Terms & Conditions Odoo, Quotation Terms & Conditions Odoo, Display Sales Terms & Condition, Show Quotation Terms & Condition Odoo, Create Sale Order Terms & Condition Module, Set SO Terms & Condition, Quote Terms & Condition Odoo.Show Sales Terms And Condition App, Create Quotation Terms And Condition Module, Set SO Terms And Condition, Sale Order Terms & Condition, Quote Terms & Condition Odoo.""",
    "depends": [

            'sale_management',
    ],

    "data": [

        'security/ir.model.access.csv',
        'security/sh_so_tnc_security.xml',
        'views/sh_terms.xml',
        'views/sale_modified.xml',
        'views/inherit_sale_report.xml',
        'views/so_preview.xml',
        'views/invoice.xml',

    ],
    "images": ["static/description/background.png", ],
    "installable": True,
    "auto_install": False,
    "application": True,
    "price": 18,
    "currency": "EUR"
}
