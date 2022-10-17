from odoo import api, fields, models


class InvoiceConditionWizard(models.TransientModel):
    _name = 'invoice.condition.wizard'
    _description = 'Invoice Condition Wizard'

    condition_type = fields.Selection([
        ('cooler', 'Cooler'),
        ('pad', 'Cooling Pad'),
        ('no_terms', 'No Terms & Conditions')], string="Format", default='cooler', required=True)

    def print_report(self):
        invoice_id = self.env.context.get('active_ids', [])
        invoice = self.env['account.move'].browse(invoice_id)
        data = {
            'invoice_id': invoice.id,
            'condition_type': self.condition_type
        }
        return self.env.ref('cells_report.action_cells_tax_invoice_report').report_action(self, data=data)
        # return self.env.ref('cells_report.action_new_report_tax_invoice').report_action(self, data=data)


class TaxInvoice(models.AbstractModel):
    _name = 'report.cells_report.report_conditional_vat_invoice'
    _description = 'Invoice'

    @api.model
    def _get_report_values(self, docids, data=None):
        print(data)
        invoice = self.env['account.move'].browse(data['invoice_id'])
        print(invoice)
        print(data['condition_type'])
        return {
            'doc_ids': docids,
            'docs': invoice,
            'condition_type': data['condition_type']
        }


