# -*- coding: utf-8 -*-
{
    'name' : 'eInvoice Panama',
    'version' : '1.0',
    'summary': 'eInvoice Panama',
    'description': """
eInvoice Panama
====================
Using The Factory HKA Web Service
    """,
    'category': 'Accounting',
    'depends' : ['account'],
    'data': [
        'data/data.xml',
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/account_tax.xml',
        'views/res_partner.xml',
        'views/res_config_settings.xml',
        'views/account_move.xml',
        'views/einvoice_composed_location.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
