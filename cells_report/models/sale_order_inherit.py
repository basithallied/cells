from odoo import api, fields, models, SUPERUSER_ID, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def get_conditions(self, terms_category_id):
        conditions = False
        if terms_category_id:
            conditions = self.env['cells.terms.conditions'].search([('term_category_id', '=', terms_category_id.id)])
            return conditions
        return conditions
