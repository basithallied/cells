{
    'name': 'Invoice Field',
    'version': '1.1',
    'summary': 'Invoice Field',
    'depends': ['base','account','e_tax_invoice_saudi_aio'],
    'data': [
        'security/ir.model.access.csv',
        'views/invoice_fields.xml',
        'views/bank_add.xml',
        ],
}
