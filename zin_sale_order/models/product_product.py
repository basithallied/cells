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

    @api.onchange('arabic_desc')
    def onchange_arabic_desc(self):
        if self.arabic_desc:
            self.product_variant_id.arabic_desc = self.arabic_desc


class ProductProduct(models.Model):
    _inherit = "product.product"

    arabic_desc = fields.Text(string="Arabic Description")

    @api.onchange('arabic_desc')
    def onchange_arabic_desc(self):
        if self.arabic_desc:
            self.product_tmpl_id.arabic_desc = self.arabic_desc
