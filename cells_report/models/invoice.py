from odoo import api, fields, models, SUPERUSER_ID, _


class AccountMove(models.Model):
    _inherit = "account.move"

    def print_conditional_invoice(self):
        invoice_id = self.env.context.get('active_ids', [])
        invoice = self.env['account.move'].search([('id', '=', self.id)])
        print(invoice, "inv")
        data = {
            'invoice_id': invoice.id,
        }
        return self.env.ref('cells_report.action_cells_tax_invoice_report').report_action(self, data=data)
        # print("hihii")
        # compose_form = self.env.ref('cells_report.view_invoice_condition_form', raise_if_not_found=False)
        # print(compose_form)
        # return {
        #     'name': _('Conditional Invoice'),
        #     'type': 'ir.actions.act_window',
        #     'view_type': 'form',
        #     'view_mode': 'form',
        #     'res_model': 'invoice.condition.wizard',
        #     'views': [(compose_form.id, 'form')],
        #     'view_id': compose_form.id,
        #     'target': 'new',
        #     # 'context': ctx,
        # }



