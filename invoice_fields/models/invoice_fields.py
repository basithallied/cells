from odoo import api, fields, models, SUPERUSER_ID, _


class AccountMoving(models.Model):
    _inherit = "account.move"

    bank_id = fields.Many2one('res.bank', string='Bank')
    conversion_rates_new = fields.Many2one('create.con', string='Conversion To')
    rate_confirm = fields.Char(string="Rate")
    job_ref = fields.Char(string='Job Reference')

    @api.onchange('conversion_rates_new')
    def _onchange_rate_swap(self):
        self.rate_confirm = self.conversion_rates_new.con_rate

    @api.onchange('rate_confirm')
    def _onchange_exchange_value(self):
        self.conversion_rates_new.con_rate = self.rate_confirm


class CreateCon(models.Model):
    _name = "create.con"
    _description = "conversion rate"

    name = fields.Char(string="name")
    con_rate = fields.Float(string="Rate")
