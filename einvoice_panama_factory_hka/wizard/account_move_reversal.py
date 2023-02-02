# -*- coding: utf-8 -*-
from odoo import api, fields, models


class AccountMoveReversal(models.TransientModel):
    _inherit = 'account.move.reversal'

    def reverse_moves(self):
        res = super(AccountMoveReversal, self).reverse_moves()
        for move in self.new_move_ids:
            move.tipo_documento = move.document_type_dict[move.move_type]
            move.naturaleza_operacion = '11'
        return res
