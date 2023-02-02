# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime


class EinvoiceDownloadPdf(models.TransientModel):
    _name = 'einvoice.download.pdf'
    _description = 'Get the document pdf from Factory HKA Web Service'
    _inherit = ['einvoice.wizard.abstract']

    def do_send(self):
        client = self._get_einvoice_zeep_client()
        data = self._get_document_status_data()
        res = client.service.DescargaPDF(**data)
        if res['codigo'] != '200':
            raise UserError(_('Something went wrong'))
        self.account_move_id.einvoice_pdf = res['documento']
