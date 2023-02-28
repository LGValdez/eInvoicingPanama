# -*- coding: utf-8 -*-
{
    'name' : 'eInvoice Panama POS',
    'version' : '1.0',
    'summary': 'eInvoice Panama POS',
    'description': """
eInvoice Panama POS
====================
Integration of POS with eInvoice Panama Factory HKA
    """,
    'category': 'Accounting',
    'depends' : ['einvoice_panama_factory_hka', 'point_of_sale'],
    'data': [
        'views/report_invoice.xml',
        'views/account_report.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
