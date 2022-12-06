from odoo import api, fields, models, SUPERUSER_ID, _


class ProductProduct(models.Model):
    _inherit = "product.product"

    def action_open_quants(self):
        if self.env.user.has_group('zin_sale_order.cells_user_inventory_adjustment'):
            res = super(ProductProduct, self).action_open_quants()
            return res

class ProductProduct(models.Model):
    _inherit = "product.template"

    arabic_desc = fields.Text(string="Arabic Description")