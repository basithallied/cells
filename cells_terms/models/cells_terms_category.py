from odoo import api, fields, models, SUPERUSER_ID, _


class TermsCategory(models.Model):
    _name = "cells.terms.category"
    _description = "Cells Terms Category"

    name = fields.Char("Name")

