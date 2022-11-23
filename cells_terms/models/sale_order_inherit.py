from odoo import api, fields, models, SUPERUSER_ID, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    terms_category_id = fields.Many2one("cells.terms.category", "Terms Category")

    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()
        if self.terms_category_id:
            invoice_vals['terms_category_id'] = self.terms_category_id.id
        return invoice_vals


