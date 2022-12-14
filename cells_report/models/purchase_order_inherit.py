from odoo import api, fields, models, SUPERUSER_ID, _


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    purchase_picking_policy = fields.Selection([
        ('direct', 'As soon as possible'),
        ('one', 'When all products are ready')],
        string='Shipping Policy', required=True, readonly=True, default='direct',
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}
        ,help="If you deliver all products at once, the delivery order will be scheduled based on the greatest "
        "product lead time. Otherwise, it will be based on the shortest.")
    customer_so = fields.Char('Customer SO')
    def get_conditions(self, terms_category_id):
        conditions = False
        if terms_category_id:
            conditions = self.env['cells.terms.conditions'].search([('term_category_id', '=', terms_category_id.id)])
            return conditions
        return conditions
