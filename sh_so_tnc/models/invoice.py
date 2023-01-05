# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import api, fields, models

# Invoice Terms And Conditions


class InvoiceInherate(models.Model):
    _inherit = 'account.move'

    term_conditions = fields.Many2one(
        'sh.so.tnc', string="Terms And Conditions")
    terms_detail = fields.Html(string="Conditions Detail")
    sh_in_report = fields.Boolean('Display in Report ??', default=True)

    @api.onchange('term_conditions')
    def _onchange_term_con(self):
        if self.term_conditions:
            self.terms_detail = self.term_conditions.terms_con
