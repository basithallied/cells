from odoo import api, fields, models, _


class SaleInvoice(models.Model):
    _inherit = "sale.order"

    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()
        print('ssssssssssssssssssssssssss')
        if self.picking_policy == 'direct':
            invoice_vals['new_picking_policy'] = 'As soon as possible'
        else:
            invoice_vals['new_picking_policy'] = 'When products are ready'
        return invoice_vals
