from odoo import api, fields, models, _


class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    terms_category_id = fields.Many2one("cells.terms.category", "Terms Category")
    shipping_method = fields.Selection([
        ('by_road', 'By Road'),
        ('by_air', 'By Air'),
        ('by_sea', 'By Sea')], string="Shipping Method", default='by_road')
