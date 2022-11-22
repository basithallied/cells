from odoo import api, fields, models, SUPERUSER_ID, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    default_product = fields.Boolean("Cells Default Product", default=True)
    arabic_name = fields.Char("Arabic Name")

    def action_open_quants(self):
        if self.env.user.has_group('zin_sale_order.cells_user_inventory_adjustment'):
            res = super(ProductTemplate, self).action_open_quants()
            return res

