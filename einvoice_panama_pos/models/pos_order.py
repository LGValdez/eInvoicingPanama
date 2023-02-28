# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _


class PosOrder(models.Model):
    _inherit = "pos.order"

    def _generate_pos_order_invoice(self):
        res = super(PosOrder, self)._generate_pos_order_invoice()
        AccountMove = self.env['account.move']
        for order in self:
            moves = AccountMove.search([
                ('ref', '=', order.name),
                ('state', '=', 'posted'),
            ])
            for move in moves:
                move.einvoice_send_and_update()
        return res
