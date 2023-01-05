# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import fields, models

# Terms And Conditions


class ShSoTnc(models.Model):
    _name = 'sh.so.tnc'
    _description = "Sh So Tnc"

    name = fields.Char('Terms',translate=True)
    terms_con = fields.Html(string="Terms & Conditions",translate=True)
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.company)
