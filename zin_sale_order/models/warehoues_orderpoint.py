from odoo import api, fields, models, tools, _


class StockOrderPoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    def reorder_notification(self):
        reorders = self.env['stock.warehouse.orderpoint'].search([('active', '=', True)])
        reordering_list = []
        for order in reorders:
            if order.qty_on_hand <= order.product_min_qty:
                reordering_list.append(order.product_id)
                mail_user = self.env.user
                mail_company = mail_user.company_id
                body = "Product " + order.product_id.name + " is reached to minimum quantity  " + \
                       str(order.qty_on_hand) + " at " + "location " + order.location_id.name
                print(body)
                mail_values = {
                    'auto_delete': True,
                    'author_id': mail_user.partner_id.id,
                    'email_from': mail_company.email_formatted,
                    'email_to': mail_company.email_formatted,
                    'body_html': body,
                    'reply_to': mail_company.email_formatted or mail_user.email_formatted,
                    'state': 'outgoing',
                    'subject': "test"
                }
                mail = self.env['mail.mail'].sudo().create(mail_values)
                mail.sudo().send()





