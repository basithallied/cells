from odoo import api, fields, models, SUPERUSER_ID, _


class TermsConditions(models.Model):
    _name = "cells.terms.conditions"
    _description = "Cells Terms & Conditions"
    _rec_name = 'type'

    name = fields.Char("Header")
    type = fields.Selection([
        ('cooler', 'Cooler'),
        ('pad', 'Cooling Pad')], string="Format", default='cooler', required=True)
    line_ids = fields.One2many('cells.terms.conditions.lines', 'term_id', "Lines")


class TermsConditionsLines(models.Model):
    _name = "cells.terms.conditions.lines"
    _description = "Cells Terms & Conditions Lines"

    term_id = fields.Many2one('cells.terms.conditions', "Terms")
    name = fields.Char("Terms")
    val_ids = fields.Many2many("cells.line.values", string="Name")


class CellsLineValues(models.Model):
    _name = "cells.line.values"
    _description = "Cells Lines Values"

    name = fields.Char("Name")


