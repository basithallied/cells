from io import StringIO, BytesIO
from odoo import api, fields, models, _
import base64
import xlsxwriter
import io


class CoolerSalesReport(models.TransientModel):
    _name = 'cooler.sales.report.wizard'
    _description = 'Cooler Sales Report'

    date_from = fields.Date("Date From", required=True)
    date_to = fields.Date("Date To", required=True)
    summary = fields.Binary('Summary')
    file_name = fields.Char('File name')

    def print_sale_report(self):
        ids = self._ids
        f_name = 'Cooler Sales Report' + '.xlsx'
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
        worksheet1.merge_range(0, 6, 0, 15, 'COOLER SALES REPORT ', center_format)
        d = str(self.date_from) + ' - ' + str(self.date_to)
        worksheet1.merge_range(2, 6, 2, 15, 'Date As of ' + d, center_format)

        default_products = self.env['product.template'].search([('default_product', '=', True)])
        worksheet1.merge_range(row, col, row + 1, col, 'NO', center_format)
        col += 1
        worksheet1.set_column(col, col, 30)
        worksheet1.merge_range(row, col, row + 1, col, 'CUSTOMER NAME', center_format)
        col += 1

        end_col = col + len(default_products.ids) - 1
        worksheet1.merge_range(row, col, row, end_col, 'COOLER SIZE', center_format)
        worksheet1.set_column(col, end_col, 5)
        f_row = row + 1
        products_dict = {}
        for product in default_products:
            worksheet1.write(f_row, col, product.name, center_format)
            products_dict[product.name] = col
            col += 1
        print(products_dict)
        worksheet1.set_column(col, col, 15)
        worksheet1.merge_range(row, col, row + 1, col, ' Payment date', center_format)
        col += 1
        worksheet1.set_column(col, col, 10)
        worksheet1.merge_range(row, col, row + 1, col, ' ملاحظات ', center_format)
        col += 1
        worksheet1.set_column(col, col, 10)
        worksheet1.merge_range(row, col, row + 1, col, ' Days', center_format)
        col += 1
        worksheet1.set_column(col, col, 10)
        worksheet1.merge_range(row, col, row + 1, col, ' Amount', center_format)
        col += 1
        worksheet1.set_column(col, col, 10)
        worksheet1.merge_range(row, col, row + 1, col, '  Received', center_format)
        col += 1
        worksheet1.set_column(col, col, 10)
        worksheet1.merge_range(row, col, row + 1, col, ' NET DUE', center_format)
        orders = self.env['sale.order'].search([('date_order', '>=', self.date_from),
                                                ('is_maintenance', '=', False)])
        count = 1
        row = 10
        d_col = 0
        for order in orders:
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

            worksheet1.write(row, d_col, count, center_format)
            d_col += 1
            worksheet1.write(row, d_col, order.partner_id.name, txt_format)
            for line in order.order_line:
                if line.product_id.name in products_dict:
                    l_col = products_dict[line.product_id.name]
                    worksheet1.write(row, int(l_col), line.product_uom_qty, center_format)
            d_col = d_col + len(default_products.ids) + 1
            worksheet1.write(row, d_col, str(payment_date), txt_format)
            worksheet1.write(row, d_col + 1, str(payment_date), txt_format)
            worksheet1.write(row, d_col + 2, amount, number)
            worksheet1.write(row, d_col + 3, amount, number)
            worksheet1.write(row, d_col + 4, paid_amount, number)
            worksheet1.write(row, d_col + 5, due_amount, number)
            row += 1
            d_col = 0
        workbook.close()
        data11 = base64.encodebytes(output.getvalue())
        self.write({'summary': data11, 'file_name': f_name})
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': ids[0],
            'res_model': 'cooler.sales.report.wizard',
            'target': 'new',
            'name': 'Cooler Sales Report'
        }
