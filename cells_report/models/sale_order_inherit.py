from odoo import api, fields, models, SUPERUSER_ID, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    bank_id = fields.Many2one('res.bank', string='Bank')

    def get_conditions(self, terms_category_id):
        conditions = False
        if terms_category_id:
            conditions = self.env['cells.terms.conditions'].search([('term_category_id', '=', terms_category_id.id)])
            return conditions
        return conditions
class ResCompany(models.Model):
    _inherit = "res.company"

    bank_id = fields.Many2one('res.bank', string='Bank')