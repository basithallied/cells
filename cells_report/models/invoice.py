from odoo import api, fields, models, SUPERUSER_ID, _


class AccountMove(models.Model):
    _inherit = "account.move"

    def print_conditional_invoice(self):
        invoice = self.env['account.move'].search([('id', '=', self.id)])
        data = {
            'invoice_id': invoice.id,
        }
        return self.env.ref('cells_report.action_cells_tax_invoice_report').report_action(self, data=data)
    def print_conditional_invoice_arabic(self):
   # merlin changed
        return self.env.ref('cells_report.action_report_invoice_arabic').report_action(self)


    def print_vendor_bill(self):
        invoice = self.env['account.move'].search([('id', '=', self.id)])
        data = {
            'invoice_id': invoice.id,
        }
        return self.env.ref('cells_report.action_cells_vendor_bill_report').report_action(self, data=data)

    def print_vendor_bill_arabic(self):
        return self.env.ref('cells_report.action_report_vendor_arabic').report_action(self)

    def get_conditions(self, terms_category_id):
        conditions = False
        if terms_category_id:
            conditions = self.env['cells.terms.conditions'].search([('term_category_id', '=', terms_category_id.id)])
            return conditions
        return conditions

