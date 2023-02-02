from odoo import models, fields, api


class EinvoiceComposedLocation(models.Model):
    _name = 'einvoice.composed.location'
    _description = 'Composed Locations Imported for eInvoice'
    _rec_name = 'display_name'

    name = fields.Char(string='Location Name')
    code = fields.Char(string='Location Code')
    display_name = fields.Char(compute='_compute_display_name', store=True)

    @api.depends('name', 'code')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f'[{record.code}] {record.name}'
