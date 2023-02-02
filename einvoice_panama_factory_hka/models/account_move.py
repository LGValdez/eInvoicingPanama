# -*- coding: utf-8 -*-
from odoo import api, fields, models
from collections import defaultdict


class AccountMove(models.Model):
    _inherit = 'account.move'

    document_type_dict = defaultdict(lambda: '01', {
        'out_invoice': '01',
        'in_invoice': '01',
        'out_refund': '06',
        'in_refund': '07',
    })

    def _get_default_document_type(self):
        return self.document_type_dict[self.env.context.get('default_move_type')]

    tipo_emision = fields.Selection([
        ('01', 'Autorización de Uso Previa (Manual)'),
        ('02', 'Autorización de Uso Previa (Contingencia)'),
        ('03', 'Autorización de Uso Posterior (Manual)'),
        ('04', 'Autorización de Uso Posterior (Contingencia)'),
    ], string='Tipo de Emisión', default='01', copy=False)
    tipo_documento = fields.Selection([
        ('01', 'Factura de Operación Interna'),
        ('02', 'Factura de Importación'),
        ('03', 'Factura de Exportación'),
        ('04', 'Nota de Crédito Referente a FE'),
        ('05', 'Nota de Débito Referente a FE'),
        ('06', 'Nota de Crédito Genérica'),
        ('07', 'Nota de Débito Genérica'),
        ('08', 'Factura de Zona Franca'),
        ('09', 'Reembolso'),
    ], string='Tipo de Documento', default=_get_default_document_type, copy=False)
    naturaleza_operacion = fields.Selection([
        ('01', 'Venta'),
        ('02', 'Exportación'),
        ('10', 'Transferencia'),
        ('11', 'Devolución'),
        ('12', 'Consignacción'),
        ('13', 'Remesa'),
        ('14', 'Entrega Gratuita'),
        ('20', 'Compra'),
        ('21', 'Importación'),
    ], string='Naturaleza de Operación', default='01', copy=False)
    tipo_operacion = fields.Selection([
        ('1', 'Salida o Venta'),
        ('2', 'Entrada o Compra'),
    ], string='Tipo de Operación', default='1', copy=False)
    destino_operacion = fields.Selection([
        ('1', 'Panamá'),
        ('2', 'Extranjero'),
    ], string='Destino de Operación', default='1', copy=False)

    einvoice_fiscal_number = fields.Char(string='Fiscal Invoice Number', copy=False)
    einvoice_unique_code = fields.Char(string='CUFE', copy=False)
    einvoice_qr_code = fields.Char(string='QR', copy=False)
    einvoice_dgi_reception_date = fields.Char(string='DGI Date Reception', copy=False)
    einvoice_dgi_protocol_number = fields.Char(string='DGI Protocol Number', copy=False)
    einvoice_processed = fields.Boolean(string='eInvoice Processed', copy=False)
    einvoice_status = fields.Char(string='Document Status', copy=False)
    einvoice_pdf = fields.Binary(string='PDF', copy=False)

    def einvoice_send_document(self):
        self.ensure_one()
        wizard = self.env['einvoice.send.document'].create({'account_move_id': self.id})
        wizard.do_send()

    def einvoice_document_status(self):
        self.ensure_one()
        wizard = self.env['einvoice.document.status'].create({'account_move_id': self.id})
        wizard.do_send()

    def einvoice_cancel_document(self):
        self.ensure_one()
        wizard = self.env['einvoice.cancel.document'].create({'account_move_id': self.id})
        wizard.do_send()

    def einvoice_download_pdf(self):
        self.ensure_one()
        wizard = self.env['einvoice.download.pdf'].create({'account_move_id': self.id})
        wizard.do_send()

    def einvoice_send_and_update(self):
        self.einvoice_send_document()
        self.einvoice_document_status()
        self.einvoice_download_pdf()
