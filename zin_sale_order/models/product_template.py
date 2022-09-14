from odoo import api, fields, models, SUPERUSER_ID, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # is_pad = fields.Boolean("Is Pad")
    default_product = fields.Boolean("Cells Default Product", default=True)
    # order_seq = fields.Integer("Product Sequence")
