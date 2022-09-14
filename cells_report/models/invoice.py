from odoo import api, fields, models, SUPERUSER_ID, _


class AccountMove(models.Model):
    _inherit = "account.move"

    def print_conditional_invoice(self):
        print("hihii")
        compose_form = self.env.ref('cells_report.view_invoice_condition_form', raise_if_not_found=False)
        print(compose_form)
        return {
            'name': _('Conditional Invoice'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'invoice.condition.wizard',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            # 'context': ctx,
        }


