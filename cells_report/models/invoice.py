from odoo import api, fields, models, SUPERUSER_ID, _


class AccountMove(models.Model):
    _inherit = "account.move"

    def print_conditional_invoice(self):
        invoice = self.env['account.move'].search([('id', '=', self.id)])
        data = {
            'invoice_id': invoice.id,
        }
        return self.env.ref('cells_report.action_cells_tax_invoice_report').report_action(self, data=data)



