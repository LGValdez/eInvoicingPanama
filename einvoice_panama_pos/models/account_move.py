# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from datetime import datetime


class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_total_items(self):
        self.ensure_one()
        return sum(l.quantity for l in self.invoice_line_ids)

    def _get_formatted_invoice_date(self):
        self.ensure_one()
        return self.einvoice_dgi_reception_date and self.einvoice_dgi_reception_date[:-6].replace("T", " ") or ""
    
    def _get_client_type(self):
        self.ensure_one()
        CLIENT_TYPE_DICT = {
            "01": "Contribuyente",
            "02": "Consumidor Final",
            "03": "Gobierno",
            "04": "Extranjero",
        }
        return self.partner_id and self.partner_id.tipo_cliente_fe and CLIENT_TYPE_DICT[self.partner_id.tipo_cliente_fe] or ""

    def change_size_page(self, items):
        DEFAULT_ROLL_LENGTH = 180
        paper_format = self.env['report.paperformat'].search([('name', '=', 'Invoice Roll')], limit=1)
        paper_format.page_height = DEFAULT_ROLL_LENGTH + (len(items) * 14)
