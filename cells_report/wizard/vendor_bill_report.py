from odoo import api, fields, models


class VendorBillReport(models.TransientModel):
    _name = 'vendor.bill.report'
    _description = 'Vendor Bill Report'

    def print_report(self):
        invoice_id = self.env.context.get('active_ids', [])
        invoice = self.env['account.move'].browse(invoice_id)
        data = {
            'invoice_id': invoice.id,
        }
        return self.env.ref('cells_report.action_cells_vendor_bill_report').report_action(self, data=data)


class TaxInvoice(models.AbstractModel):
    _name = 'report.cells_report.report_cells_vendor_bill'
    _description = 'Invoice'

    @api.model
    def _get_report_values(self, docids, data=None):
        invoice = self.env['account.move'].search([('id', '=', data['invoice_id'])])
        conditions = False
        if invoice.terms_category_id.id:
            conditions = self.env['cells.terms.conditions'].search(
                [('term_category_id', '=', invoice.terms_category_id.id)])
        return {
            'doc_ids': docids,
            'docs': invoice,
            'conditions': conditions
        }


