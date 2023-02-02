# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    service_url = fields.Char(
        string="Service URL", config_parameter='einvoice_panama_factory_hka.service_url')
    token_user = fields.Char(
        string="Token User", config_parameter='einvoice_panama_factory_hka.token_user')
    token_password = fields.Char(
        string="Token Password", config_parameter='einvoice_panama_factory_hka.token_password')

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'einvoice_panama_factory_hka.service_url', self.service_url)
        self.env['ir.config_parameter'].sudo().set_param(
            'einvoice_panama_factory_hka.token_user', self.token_user)
        self.env['ir.config_parameter'].sudo().set_param(
            'einvoice_panama_factory_hka.token_password', self.token_password)
