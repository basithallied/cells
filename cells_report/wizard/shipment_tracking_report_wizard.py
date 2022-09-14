from io import StringIO, BytesIO
from odoo import api, fields, models, _
import base64
import xlsxwriter
import io


class ShipmentTrackingWizard(models.TransientModel):
    _name = 'shipment.tracking.report.wizard'
    _description = 'Shipment Tracking Report Wizard'

    date_from = fields.Date("Date From", required=True)
    date_to = fields.Date("Date To", required=True)
    partner_id = fields.Many2one('res.partner', "Vendor")
    summary = fields.Binary('Summary')
    file_name = fields.Char('File name')

    def print_shipment_report(self):
        ids = self._ids
        f_name = 'Shipment Tracking Report' + '.xlsx'
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet1 = workbook.add_worksheet('Sheet')
        center_format = workbook.add_format({'bold': 1, 'align': 'center', 'valign': 'vcenter'})
        # center_format = workbook.add_format({'bold': 1, 'align': 'center', 'valign': 'vcenter', 'bg_color': '00ffff'})
        txt_format = workbook.add_format({'align': 'center', 'valign': 'vcenter'})
        number = workbook.add_format({'align': 'center', 'num_format': "#,##0.00"})
        worksheet1.set_column(0, 8, 10)

        row = 8
        col = 0

        product_image = io.BytesIO(base64.b64decode(self.env.user.company_id.logo))
        worksheet1.insert_image(0, 3, "image.png", {'image_data': product_image, 'x_scale': 0.5, 'y_scale': 0.5})
        worksheet1.merge_range(0, 6, 0, 15, 'SHIPMENT TRACKING REPORT ', center_format)
        d = str(self.date_from) + ' - ' + str(self.date_to)
        worksheet1.merge_range(2, 6, 2, 15, 'Date As of ' + d, center_format)
        if self.partner_id:
            purchases = self.env['purchase.order'].search([('date_order', '>=', self.date_from),
                                                                  ('date_order', '<=', self.date_to),
                                                                  ('partner_id', '=', self.partner_id.id)])
        else:
            purchases = self.env['purchase.order'].search([('date_order', '>=', self.date_from),
                                                                  ('date_order', '<=', self.date_to)])
        worksheet1.set_column(1, 10, 20)
        worksheet1.write(row, col, 'NO', center_format)
        worksheet1.write(row, col + 1, 'Vendor Name', center_format)
        worksheet1.write(row, col + 2, 'Item', center_format)
        worksheet1.write(row, col + 3, 'PO Number', center_format)
        worksheet1.write(row, col + 4, 'PO Date', center_format)
        worksheet1.write(row, col + 5, '1st Payment Date', center_format)
        worksheet1.write(row, col + 6, 'QTY Of Container', center_format)
        worksheet1.write(row, col + 7, 'Total Amount', center_format)
        worksheet1.write(row, col + 8, 'Payed Amount', center_format)
        worksheet1.write(row, col + 9, 'Balance Amount', center_format)
        worksheet1.write(row, col + 10, 'Bill Of Landing NO', center_format)
        worksheet1.write(row, col + 11, 'Shipping CO', center_format)
        worksheet1.write(row, col + 12, 'Shipping Date', center_format)
        worksheet1.write(row, col + 13, 'Expected Date', center_format)
        worksheet1.write(row, col + 14, 'Port', center_format)
        worksheet1.write(row, col + 15, 'Arrival Date Riyadh', center_format)
        worksheet1.write(row, col + 16, 'Update Check For ETA', center_format)
        worksheet1.write(row, col + 17, 'Amount Paid', center_format)
        worksheet1.write(row, col + 18, 'Original Documents', center_format)
        worksheet1.write(row, col + 19, 'Copy Documents', center_format)
        worksheet1.write(row, col + 20, 'Saber Certificate', center_format)
        worksheet1.write(row, col + 21, 'Status', center_format)
        worksheet1.write(row, col + 22, 'Link', center_format)

        count = 1
        row += 1
        for order in purchases:
            if len(order.invoice_ids) <= 1:
                payment_date = order.invoice_ids.invoice_date if order.invoice_ids.invoice_date else ''
                amount = order.invoice_ids.amount_total if order.invoice_ids.amount_total else 0
                due_amount = order.invoice_ids.amount_residual if order.invoice_ids.amount_residual else 0
                paid_amount = amount - due_amount
            else:
                payment_date = [invoice.name for invoice in order.invoice_ids]
                amount = [invoice.amount_total for invoice in order.invoice_ids]
                due_amount = [invoice.amount_residual for invoice in order.invoice_ids]
                paid_amount = [invoice.amount_total for invoice in order.invoice_ids]
            original_documents = "NO"
            copy_documents = "NO"
            if order.original_documents:
                original_documents = "YES"
            if order.copy_documents:
                copy_documents = "YES"
            col = 0
            item = ''
            for line in order.order_line:
                item += line.product_id.name
                item += ', '
            worksheet1.write(row, col, count, txt_format)
            worksheet1.write(row, col + 1, order.partner_id.name, txt_format)
            worksheet1.write(row, col + 2, item, number)
            worksheet1.write(row, col + 3, order.name, number)
            worksheet1.write(row, col + 4, str(order.date_order), number)
            worksheet1.write(row, col + 5, str(payment_date), number)
            worksheet1.write(row, col + 6, order.container_qty, number)
            worksheet1.write(row, col + 7, amount, number)
            worksheet1.write(row, col + 8, paid_amount, number)
            worksheet1.write(row, col + 9, due_amount, number)
            worksheet1.write(row, col + 10, order.bill_landing_no, number)
            worksheet1.write(row, col + 11, order.shipping_company_id.name, number)
            worksheet1.write(row, col + 12, str(order.shipping_date), number)
            worksheet1.write(row, col + 13, str(order.expected_date), number)
            worksheet1.write(row, col + 14, order.port, number)
            worksheet1.write(row, col + 15, str(order.arrival_date_riyadh), number)
            worksheet1.write(row, col + 16, '', number)
            worksheet1.write(row, col + 17, '', number)
            worksheet1.write(row, col + 18, original_documents, number)
            worksheet1.write(row, col + 19, copy_documents, number)
            worksheet1.write(row, col + 20, '', number)
            worksheet1.write(row, col + 21, order.state, number)
            worksheet1.write(row, col + 22, order.tracking_link, number)
            row += 1
            count += 1
        workbook.close()
        data11 = base64.encodebytes(output.getvalue())
        self.write({'summary': data11, 'file_name': f_name})
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': ids[0],
            'res_model': 'shipment.tracking.report.wizard',
            'target': 'new',
            'name': 'Shipment Tracking Report'
        }

