from odoo import _, api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    user_id = fields.Many2one('res.users', string='Responsible User')


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    user_id = fields.Many2one('res.users', string='Responsible User', related='move_id.user_id')