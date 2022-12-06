from odoo import api, fields, models, SUPERUSER_ID, _


class TermsConditions(models.Model):
    _name = "cells.terms.conditions"
    _description = "Cells Terms Conditions"

    name = fields.Char("Name")
    term_category_id = fields.Many2one('cells.terms.category', "Category", required=True)
    line_ids = fields.One2many('cells.terms.condition.lines', 'term_id', "Term Lines")
    language = fields.Selection([('english', 'English'), ('arabic', 'Arabic')], 'Language', default='english')


class TermsConditionsLines(models.Model):
    _name = "cells.terms.condition.lines"
    _description = "Cells Terms Condition Lines"

    term_id = fields.Many2one('cells.terms.conditions', string="Term")
    description = fields.Char("Description")
