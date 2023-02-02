# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime


class EinvoiceDocumentStatus(models.TransientModel):
    _name = 'einvoice.document.status'
    _description = 'Get the document status from Factory HKA Web Service'
    _inherit = ['einvoice.wizard.abstract']

    def do_send(self):
        client = self._get_einvoice_zeep_client()
        data = self._get_document_status_data()
        res = client.service.EstadoDocumento(**data)
        if res['codigo'] != '200':
            raise UserError(_('Something went wrong'))
        self.account_move_id.einvoice_status = res['estatusDocumento']
