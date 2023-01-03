try:
   import qrcode
except ImportError:
   qrcode = None
try:
   import base64
except ImportError:
   base64 = None
from odoo import api, fields, models, SUPERUSER_ID, _
import base64


class AccountMove(models.Model):
    _inherit = "account.move"

    l10n_sa_qr_code_str = fields.Char('QR Code', compute="_generate_qr")

    def _generate_qr(self):
        "method to generate QR code"
        def get_qr_encoding(tag, field):
            company_name_byte_array = field.encode('UTF-8')
            company_name_tag_encoding = tag.to_bytes(length=1, byteorder='big')
            company_name_length_encoding = len(company_name_byte_array).to_bytes(length=1, byteorder='big')
            return company_name_tag_encoding + company_name_length_encoding + company_name_byte_array

        for record in self:
            qr_code_str = ''
            if record.company_id.vat:
                company_name_enc = get_qr_encoding(1, record.company_id.name)
                company_vat_enc = get_qr_encoding(2, record.company_id.vat)
                # time_sa = fields.Datetime.context_timestamp(self.with_context(tz='Asia/Riyadh'),
                #                                             record.l10n_sa_confirmation_datetime)
                # timestamp_enc = get_qr_encoding(3, time_sa.isoformat())
                invoice_total_enc = get_qr_encoding(4, str(record.amount_total))
                total_vat_enc = get_qr_encoding(5, str(
                    record.currency_id.round(record.amount_total - record.amount_untaxed)))
                print("total_vat_enc", total_vat_enc)
                str_to_encode = company_name_enc + company_vat_enc + invoice_total_enc + total_vat_enc
                print("str_to_encode", str_to_encode)

                qr_code_str = base64.b64encode(str_to_encode).decode('UTF-8')
            record.l10n_sa_qr_code_str = qr_code_str
            print("l10n_sa_qr_code_str", qr_code_str)

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