# -*- coding: utf-8 -*-

from odoo import http 
from odoo import tools, SUPERUSER_ID
from odoo.http import request
from odoo.addons.web.controllers.main import ensure_db, Home
from odoo.tools.translate import _

 
class HomeLogin(Home):

    @http.route()
    def web_login(self, redirect=None, **kw):
        ensure_db()
        if request.httprequest.method == 'POST':
            request.params['login_success'] = False
            ip = kw.get('ip')
            uid = request.env['res.users'].sudo().search([('login','=',request.params['login'])], limit=1)
            if uid:
                ips = request.env['allowed.ip.user'].sudo().search([('user_id','=',uid.id)])
                if ips:
                    request.params['login_success'] = False
                    values = request.params.copy()

                    mapped = ips.filtered(lambda rec_ip: rec_ip.ip_id.name==ip)
                    if not mapped:
                        if not request.uid:
                            request.uid = request.env['ir.model.data'].sudo().get_object('base', 'public_user').id
                        values['error'] = ("You are trying to log in from an IP address that is not allowed. Please contact the Administrator for Access.")
                        return request.render('web.login', values)
        return super(HomeLogin, self).web_login(redirect, **kw)