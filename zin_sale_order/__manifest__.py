{
    'name': 'Zin Sale Order',
    'version': '15',
    'sequence': 1,
    'category': 'Sale',
    'summary': 'Sale order customisation',

    'description': """
    
     """,
    "author": "Zinfog code labs",
    "email": '',
    'depends': ['base', 'sale', 'product', 'sales_team', 'purchase', 'stock'],

    'data': [
        # 'security/ir.model.access.csv',
        'data/maintenance_order_seq.xml',
        'views/sale_order_view.xml',
        'views/product_template_view.xml',
        'views/purchase_order_view.xml',
        'views/cells_security.xml',
        'views/stock_inventory.xml',
        'views/reorder_cron.xml',
        'views/stock_move_inherit.xml'

    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
