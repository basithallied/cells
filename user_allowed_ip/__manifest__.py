# -*- coding: utf-8 -*-
#╔══════════════════════════════════════════════════════════════════════╗
#║                                                                      ║
#║                  ╔═══╦╗       ╔╗  ╔╗     ╔═══╦═══╗                   ║
#║                  ║╔═╗║║       ║║ ╔╝╚╗    ║╔═╗║╔═╗║                   ║
#║                  ║║ ║║║╔╗╔╦╦══╣╚═╬╗╔╬╗ ╔╗║║ ╚╣╚══╗                   ║
#║                  ║╚═╝║║║╚╝╠╣╔╗║╔╗║║║║║ ║║║║ ╔╬══╗║                   ║
#║                  ║╔═╗║╚╣║║║║╚╝║║║║║╚╣╚═╝║║╚═╝║╚═╝║                   ║
#║                  ╚╝ ╚╩═╩╩╩╩╩═╗╠╝╚╝╚═╩═╗╔╝╚═══╩═══╝                   ║
#║                            ╔═╝║     ╔═╝║                             ║
#║                            ╚══╝     ╚══╝                             ║
#║                  SOFTWARE DEVELOPED AND SUPPORTED BY                 ║
#║                ALMIGHTY CONSULTING SOLUTIONS PVT. LTD.               ║
#║                      COPYRIGHT (C) 2016 - TODAY                      ║
#║                      https://www.almightycs.com                      ║
#║                                                                      ║
#╚══════════════════════════════════════════════════════════════════════╝
{
    'name': "User Login Restriction based on IP",
    'category': "web",
    'version': "1.0.1",
    'summary': """Allow Some Users to Login from selected IP.""",
    'description': """Allow Some Users to Login from selected IP.
    Block User by IP
    Block IP
    IP Block
    Restrict IP
    User Access by IP
    login block by IP
    IP Address
    Access Restriction
    Access Block
    Secure odoo
    Secure Login
    Allowed IP
    """,
    'author': 'Almighty Consulting Solutions Pvt. Ltd.',
    'support': 'info@almightycs.com',
    'website': 'https://www.almightycs.com',
    'license': 'OPL-1',
    'depends': ['web', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'view/users_view.xml',
        'view/template.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'user_allowed_ip/static/src/js/login.js'
        ]
    },
    'sequence': 1,
    'images': [
        'static/description/accessed_by_someone.jpg',
    ],
    'installable': True,
    "price": 20,
    "currency": "USD",
}
