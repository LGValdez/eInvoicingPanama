# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    tipo_cliente_fe = fields.Selection([
        ("01", "Contribuyente"),
        ("02", "Consumidor Final"),
        ("03", "Gobierno"),
        ("04", "Extranjero"),
    ], string='Tipo Cliente FE')
    tipo_contribuyente = fields.Selection([
        ("1", "Natural"),
        ("2", "Jurídico"),
    ], string='Tipo Contribuyente')
    ruc_validator = fields.Char(string='Digito Verificador RUC')
    composed_location_id = fields.Many2one('einvoice.composed.location', string='Composed Location')
