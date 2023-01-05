# -*- coding: utf-8 -*-

from odoo import api, fields, models


class AllowedIP(models.Model):
    _name = 'allowed.ip'
    _description = "Allowed IP"

    name = fields.Char(size=256, string='IP', required=True)
    description = fields.Text()
    ip_ids = fields.One2many('allowed.ip.user', 'ip_id', string="Allowed IP")
    

class AllowedIPUser(models.Model):
    _name = 'allowed.ip.user'
    _description = "Allowed IP Users"

    user_id = fields.Many2one('res.users', string='User', required=True)
    ip_id = fields.Many2one('allowed.ip', string='IP', required=True)


class ResUsers(models.Model):
    _inherit = 'res.users'

    ip_ids = fields.One2many('allowed.ip.user', 'user_id', string="Allowed IP")
