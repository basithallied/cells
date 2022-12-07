{
    'name': 'Cells Reports',
    'version': '15',
    'sequence': 1,
    'category': 'Sale',
    'summary': 'Reports',

    'description': """
    
     """,
    "author": "Zinfog code labs",
    "email": '',
    'depends': ['base', 'sale', 'product', 'sales_team', 'purchase', 'web', 'cells_terms'],

    'data': [
        'security/ir.model.access.csv',
        'views/cooler_sales_report_view.xml',
        'views/cooler_maintenance_wizard_view.xml',
        'views/shipment_tracking_wizard_view.xml',
        'views/conditional_tax_invoice_view.xml',
        'report/report_purchase_quotation.xml',
        'report/cells_invoice_layout.xml',
        'report/cells_vat_invoice_template.xml',
        'report/cells_quotation_layout.xml',
        'report/report_saleorder_document.xml',
        'report/cells_purchase_layout.xml',
        'report/report_purchaseorder_document.xml',
        'report/report_saleorder_arabic.xml',
        'report/report.xml',
        'report/cells_vendor_bill_report.xml',
        'report/invoice_report_arabic.xml',
        'report/report_purchaseorder_arabic.xml'

    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    "assets": {
        "web.assets_common": [
            "cells_report/static/src/css/style.css",
        ],
    }


}
