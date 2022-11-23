from odoo import api, fields, models, _


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    terms_category_id = fields.Many2one("cells.terms.category", "Terms Category")
