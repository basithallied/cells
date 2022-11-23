{
    'name': 'Cells Terms & Conditions',
    'version': '15',
    'sequence': 1,
    'category': 'Sale',
    'summary': 'Cells Terms and Conditions',

    'description': """
    
     """,
    "author": "Zinfog code labs",
    "email": '',
    'depends': ['base', 'sale', 'sales_team', 'account'],

    'data': [
        'security/ir.model.access.csv',
        'views/cells_terms_category.xml',
        'views/cells_term_conditions_view.xml',
        'views/sale_order_inherit_view.xml',
        'views/account_move_inherit_view.xml'
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
