# -*- coding: utf-8 -*-
from odoo import api, fields, models


class AccountTax(models.Model):
    _inherit = 'account.tax'

    einvoice_tax_code = fields.Selection([
        ('00', 'Extento'),
        ('01', '7%'),
        ('02', '10%'),
        ('03', '15%'),
    ], string='Código Facturación Electrónica', default='00')
