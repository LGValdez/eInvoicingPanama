# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import datetime
import zeep


class EinvoiceSendDocument(models.TransientModel):
    _name = 'einvoice.send.document'
    _description = 'Send the document to the Factory HKA Web Service'
    _inherit = ['einvoice.wizard.abstract']

    def get_next_einvoice_number_sequence(self):
        if self.account_move_id.tipo_documento in ('04', '06'):
            sequence_id = 'einvoice_panama_factory_hka.sequence_electronic_credit_notes'
        elif self.account_move_id.tipo_documento in ('05', '07'):
            sequence_id = 'einvoice_panama_factory_hka.sequence_electronic_debit_notes'
        else:
            sequence_id = 'einvoice_panama_factory_hka.sequence_electronic_invoices'
        return self.env.ref(sequence_id)

    def get_invoice_data(self):
        invoice = self.account_move_id
        token_user, token_password = self._get_einvoice_token_credentials()
        amount_total = "{:.2f}".format(invoice.amount_total)
        amount_tax = "{:.2f}".format(invoice.amount_tax)
        amount_untaxed = "{:.2f}".format(invoice.amount_untaxed)
        einvoice_number_sequence = self.get_next_einvoice_number_sequence()
        information_interest = self.information_interest(invoice)
        next_invoice_number = invoice.einvoice_fiscal_number or einvoice_number_sequence.next_by_id()
        data = {
            "tokenEmpresa": token_user,
            "tokenPassword": token_password,
            "documento": {
                "codigoSucursalEmisor": "0000",
                "tipoSucursal": "1",
                "datosTransaccion": {
                    "tipoEmision": invoice.tipo_emision,
                    "tipoDocumento": invoice.tipo_documento,
                    "numeroDocumentoFiscal": next_invoice_number,
                    "puntoFacturacionFiscal": "001",
                    "naturalezaOperacion": invoice.naturaleza_operacion,
                    "tipoOperacion": int(invoice.tipo_operacion),
                    "destinoOperacion": int(invoice.destino_operacion),
                    "formatoCAFE": 1,
                    "entregaCAFE": 1,
                    "envioContenedor": 1,
                    "procesoGeneracion": 1,
                    "tipoVenta": 1,
                    "informacionInteres": information_interest,
                    "fechaEmision": datetime.now().strftime("%Y-%m-%dT%H:%M:%S-05:00"),
                    "cliente": {
                        "tipoClienteFE": invoice.partner_id.tipo_cliente_fe,
                        "tipoContribuyente": int(invoice.partner_id.tipo_contribuyente),
                        "numeroRUC": invoice.partner_id.vat,
                        "pais": "PA",
                        "correoElectronico1": invoice.partner_id.email,
                        "razonSocial": invoice.partner_id.name,
                        "direccion": invoice.partner_id.street,
                    },
                },
                "listaItems": {
                    "item": [{
                        "descripcion": line.name,
                        "cantidad": "{:.2f}".format(line.quantity),
                        "precioUnitario": "{:.2f}".format(line.price_unit),
                        "precioUnitarioDescuento": " ",
                        "precioItem": "{:.2f}".format(line.price_subtotal),
                        "valorTotal": "{:.2f}".format(line.price_total),
                        "codigoGTIN": "0",
                        "codigoGTINInv": "0",
                        "cantGTINCom": "0.99",
                        "cantGTINComInv": "1.00",
                        "tasaITBMS": line.tax_ids and line.tax_ids[0].einvoice_tax_code or "00",
                        "valorITBMS": "{:.2f}".format(abs(line.price_total - line.price_subtotal)),
                    } for line in invoice.invoice_line_ids]
                },
                "totalesSubTotales": {
                    "totalPrecioNeto": amount_untaxed,
                    "totalITBMS": amount_tax,
                    "totalMontoGravado": amount_tax,
                    "totalDescuento": "",
                    "totalAcarreoCobrado": "",
                    "valorSeguroCobrado": "",
                    "totalFactura": amount_total,
                    "totalValorRecibido": amount_total,
                    "vuelto": "0.00",
                    "tiempoPago": "1",
                    "nroItems": len(invoice.invoice_line_ids),
                    "totalTodosItems": amount_total,
                    "listaFormaPago": {
                        "formaPago": [{
                            "formaPagoFact": "02",
                            "descFormaPago": " ",
                            "valorCuotaPagada": amount_total,
                        }]
                    }
                }
            }
        }
        if invoice.partner_id.ruc_validator:
            data["documento"]["datosTransaccion"]["cliente"]["digitoVerificadorRUC"] = invoice.partner_id.ruc_validator
        if invoice.partner_id.composed_location_id:
            data["documento"]["datosTransaccion"]["cliente"][
                "codigoUbicacion"] = invoice.partner_id.composed_location_id.code
            location_codes = invoice.partner_id.composed_location_id.code.split("-")
            data["documento"]["datosTransaccion"]["cliente"]["provincia"] = location_codes[0]
            data["documento"]["datosTransaccion"]["cliente"]["distrito"] = location_codes[1]
            data["documento"]["datosTransaccion"]["cliente"]["corregimiento"] = location_codes[2]
        return data

    def update_invoice(self, res, data):
        invoice_update_values = {
            'einvoice_fiscal_number': data['documento']['datosTransaccion']['numeroDocumentoFiscal'],
            'einvoice_unique_code': res['cufe'],
            'einvoice_qr_code': res['qr'],
            'einvoice_dgi_reception_date': res['fechaRecepcionDGI'],
            'einvoice_dgi_protocol_number': res['nroProtocoloAutorizacion'],
            'einvoice_processed': True,
        }
        self.account_move_id.update(invoice_update_values)

    def do_send(self):
        client = self._get_einvoice_zeep_client()
        data = self.get_invoice_data()
        res = client.service.Enviar(**data)
        if res['codigo'] != '200':
            raise UserError(res['mensaje'])
        self.update_invoice(res, data)

    def information_interest(self, invoice):
        return "Pagos a: Importadora GBG, S.A." \
               "Banco General " \
               "Cuenta Corriente " \
               "0395011404870 " \
               "enviar comprobante a: gerencia@gbgsuperfood.com, " \
               "Vendedor:" + invoice.invoice_user_id.partner_id.name if invoice.invoice_user_id else ""
