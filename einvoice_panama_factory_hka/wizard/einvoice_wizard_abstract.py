# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime
import zeep


class EinvoiceWizardAbstract(models.AbstractModel):
    _name = 'einvoice.wizard.abstract'
    _description = 'Factory HKA Web Service abstract model for connection'

    account_move_id = fields.Many2one('account.move', string='Invoice')

    def _get_datos_documento(self):
        invoice = self.account_move_id
        return {
            "codigoSucursalEmisor": "0000",
            "puntoFacturacionFiscal": "001",
            "numeroDocumentoFiscal": invoice.einvoice_fiscal_number,
            "tipoDocumento": invoice.tipo_documento,
            "tipoEmision": invoice.tipo_emision,
        }

    def _get_document_status_data(self):
        token_user, token_password = self._get_einvoice_token_credentials()
        data = {
            "tokenEmpresa": token_user,
            "tokenPassword": token_password,
            "datosDocumento": self._get_datos_documento()

        }
        return data

    def _get_einvoice_zeep_client(self):
        wsdl = self.env['ir.config_parameter'].sudo().get_param(
            'einvoice_panama_factory_hka.service_url')
        client = zeep.Client(wsdl=wsdl)
        return client

    def _get_einvoice_token_credentials(self):
        token_user = self.env['ir.config_parameter'].sudo().get_param(
            'einvoice_panama_factory_hka.token_user')
        token_password = self.env['ir.config_parameter'].sudo().get_param(
            'einvoice_panama_factory_hka.token_password')
        return token_user, token_password
