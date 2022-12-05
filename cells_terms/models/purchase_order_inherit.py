from odoo import api, fields, models, _


class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    terms_category_id = fields.Many2one("cells.terms.category", "Terms Category")
