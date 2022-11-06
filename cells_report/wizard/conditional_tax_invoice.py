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
        print(invoice.l10n_sa_qr_code_str, "sddddddd")
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
        invoice = self.env['account.move'].browse(data['invoice_id'])
        term = False
        if data['condition_type'] == 'cooler':
            cells_term_id = self.env['ir.config_parameter'].sudo().get_param('zin_sale_order.cooler_term_id')
            term = self.env['cells.terms.conditions'].sudo().browse(int(cells_term_id))
        elif data['condition_type'] == 'pad':
            cells_term_id = self.env['ir.config_parameter'].sudo().get_param('zin_sale_order.pad_term_id')
            term = self.env['cells.terms.conditions'].sudo().browse(int(cells_term_id))
        print(term)
        return {
            'doc_ids': docids,
            'docs': invoice,
            'condition_type': data['condition_type'],
            'term': term
        }


