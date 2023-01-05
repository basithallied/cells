from odoo import api, fields, models, SUPERUSER_ID, _


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    term_conditions = fields.Many2one(
        'sh.so.tnc', string="Terms And Conditions")
    terms_detail = fields.Html(string="Conditions Detail")
    sh_in_report = fields.Boolean('Display in Report ??', default=True)

    @api.onchange('term_conditions')
    def _onchange_term_con(self):
        if self.term_conditions:
            self.terms_detail = self.term_conditions.terms_con

    def get_conditions(self, terms_category_id):
        conditions = False
        if terms_category_id:
            conditions = self.env['cells.terms.conditions'].search([('term_category_id', '=', terms_category_id.id)])
            return conditions
        return conditions
