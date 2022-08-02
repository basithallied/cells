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
    'depends': ['base', 'sale', 'product', 'sales_team', 'purchase', 'web'],

    'data': [
        'security/ir.model.access.csv',
        'views/cooler_sales_report_view.xml',
        'views/cooler_maintenance_wizard_view.xml',
        'report/report_purchase_quotation.xml',

    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
