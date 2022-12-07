# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import qrcode
import base64
import io
from odoo import http
from num2words import num2words
from odoo.tools.misc import formatLang, format_date, get_lang
from odoo.exceptions import UserError
from datetime import timedelta, datetime


class AccountMove(models.Model):
    _inherit = 'account.move'

    # merlin added
    ship_to_city = fields.Char('Ship To City')

    arabic_name = fields.Char(string='Arabic Name')
    arabic_relate = fields.Char('Relate')
    date_due = fields.Date('Date Due')
    invoice_date_supply = fields.Date('Invoice Period')
    journals = fields.Char(string='Journal')
    invoice_date_supply_new = fields.Date()
    contract_no = fields.Text(string="Your Order/Contract No")
    our_code_no = fields.Text(string="Job Code")
    dates = fields.Char(string='dates', compute='_compute_dates',)
    new_tax_exclude = fields.Char(string='Tax Excluded', compute='_compute_new_tax_exclude')
    new_tax_exclude_tree = fields.Char(string='Tax Excluded')
    new_tax_only = fields.Char(string='Tax Only')

    # merlin added

    # category_ids = fields.Many2one('category.master', string="Category", tracking=True)
    # terms_condition_ids = fields.One2many('terms.description.desc', 'terms_condition_id',
    #                                       string="Terms and Conditions", tracking=True)


    def _compute_new_tax_exclude(self):
        print("start computing")
        for rec in self:
            if rec.currency_id.name == 'USD' or rec.currency_id.name == 'EUR':
                discount_total = 0
                for line in rec.invoice_line_ids:
                    discount_total = discount_total + (line.price_unit + line.quantity) - line.price_subtotal
                discount_before_total = rec.amount_untaxed + discount_total
                rec.new_tax_exclude = round(rec.amount_residual * rec.conversion_rates_new.con_rate, 2)
                rec.new_tax_exclude_tree = str(rec.new_tax_exclude) + ' ' + 'SAR'
                rec.new_tax_exclude_tree = rec.amount_untaxed
                print(rec.new_tax_exclude_tree,"rec.new_tax_exclude_tree")

                rec.new_tax_only = round((rec.amount_total - rec.amount_untaxed) * rec.conversion_rates_new.con_rate, 2)
            else:
                rec.new_tax_exclude = round(rec.amount_residual)
                rec.new_tax_exclude_tree = str(rec.amount_residual) + ' ' + 'SAR'
                rec.new_tax_only = round(rec.amount_total - rec.amount_untaxed, 2)

    def _compute_dates(self):
        inv_date = self.invoice_payment_term_id.line_ids.days
        if self.invoice_date:
            result = self.invoice_date + timedelta(days=inv_date)
            new_date = result.strftime("%d-%b-%Y")
            self.dates = new_date

    @api.onchange('currency_id')
    def _onchange_currency_id(self):
        if self.currency_id.name != 'SAR':
            find_sar = self.env['create.con'].search([('name', '=', 'SAR')])
            self.conversion_rates_new = find_sar.id
            self.rate_confirm = find_sar.con_rate

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        list1 = []
        h = []
        for rec in self:
            if rec.partner_id:
                rec.arabic_name = rec.partner_id.arabic_name
                rec.journals = rec.partner_id.journal_id.name
                list1 = rec.partner_id.bank_ids

        for rec in list1:
            h.append(rec.bank_id.id)
        domain = {'bank_id': [('id', 'in', h)]}
        return {'domain': domain}

    def get_product_arabic_name(self,pid):
        translation = self.env['ir.translation'].search([
            ('name','=','product.product,name'),('state','=','translated'),
            ('res_id','=',pid)])
        if translation :
            return translation.value
        else: 
            product = self.env['product.product'].browse(int(pid))
            translation = self.env['ir.translation'].search([
                ('name','=','product.product,name'),('state','=','translated'),
                ('res_id','=',product.product_tmpl_id.id)])
            if translation :
                return translation.value
        return ''

    def amount_word(self, amount):
        language = self.partner_id.lang or 'en'
        language_id = self.env['res.lang'].search([('code', '=', 'ar_001')])
        if language_id:
            language = language_id.iso_code
        amount_str =  str('{:2f}'.format(amount))
        amount_str_splt = amount_str.split('.')
        before_point_value = amount_str_splt[0]
        after_point_value = amount_str_splt[1][:2]           
        before_amount_words = num2words(int(before_point_value),lang=language)
        after_amount_words = num2words(int(after_point_value),lang=language)
        amount = before_amount_words + ' ' + after_amount_words
        return amount

    def amount_total_words(self, amount):
        words_amount = self.currency_id.amount_to_text(amount)
        return words_amount

    # -----------------
    @api.depends('amount_total', 'amount_untaxed', 'l10n_sa_confirmation_datetime', 'company_id', 'company_id.vat')
    def _compute_qr_code_str(self):
        """ Generate the qr code for Saudi e-invoicing. Specs are available at the following link at page 23
        https://zatca.gov.sa/ar/E-Invoicing/SystemsDevelopers/Documents/20210528_ZATCA_Electronic_Invoice_Security_Features_Implementation_Standards_vShared.pdf
        """

        def get_qr_encoding(tag, field):
            company_name_byte_array = field.encode('UTF-8')
            company_name_tag_encoding = tag.to_bytes(length=1, byteorder='big')
            company_name_length_encoding = len(company_name_byte_array).to_bytes(length=1, byteorder='big')
            return company_name_tag_encoding + company_name_length_encoding + company_name_byte_array

        for record in self:
            qr_code_str = ''
            if record.l10n_sa_confirmation_datetime and record.company_id.vat:
                seller_name_enc = get_qr_encoding(1, record.company_id.display_name)
                company_vat_enc = get_qr_encoding(2, record.company_id.vat)
                time_sa = fields.Datetime.context_timestamp(self.with_context(tz='Asia/Riyadh'),
                                                            record.l10n_sa_confirmation_datetime)
                timestamp_enc = get_qr_encoding(3, time_sa.isoformat())
                # invoice_total_enc = get_qr_encoding(4, str(record.amount_total))
                # print("invoice_total_enc", invoice_total_enc)
                invoice_total_enc = get_qr_encoding(4, str(record.new_tax_exclude))
                # total_vat_enc = get_qr_encoding(5, str(
                #     record.currency_id.round(record.amount_total - record.amount_untaxed)))
                total_vat_enc = get_qr_encoding(5, str(record.new_tax_only))
                print("total_vat_enc", total_vat_enc)
                str_to_encode = seller_name_enc + company_vat_enc + timestamp_enc + invoice_total_enc + total_vat_enc
                qr_code_str = base64.b64encode(str_to_encode).decode('UTF-8')
            record.l10n_sa_qr_code_str = qr_code_str

# -----------

    def action_invoice_sent(self):
        """ Open a window to compose an email, with the edi invoice template
            message loaded by default
        """
        self.ensure_one()
        template = self.env.ref('e_tax_invoice_saudi_aio.email_template_edi_invoice_etir', False)
        lang = get_lang(self.env)
        if template and template.lang:
            lang = template._render_template(template.lang, 'account.move', self.id)
        else:
            lang = lang.code
        compose_form = self.env.ref('account.account_invoice_send_wizard_form', raise_if_not_found=False)
        ctx = dict(
            default_model='account.move',
            default_res_id=self.id,
            default_res_model='account.move',
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_composition_mode='comment',
            mark_invoice_as_sent=True,
            custom_layout="mail.mail_notification_paynow",
            model_description=self.with_context(lang=lang).type_name,
            force_email=True
        )
        return {
            'name': _('Send Invoice'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.invoice.send',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }

class ResBankInherit(models.Model):
    _inherit = 'res.bank'

    def name_get(self):
        result = []
        for bank in self:
            lst_str = str(bank.acc_no)
            name = bank.name + (bank.bic and (' - ' + bank.bic + ' ' + lst_str[-4:]) or '')
            result.append((bank.id, name))
        return result


class ResPartner(models.Model):
    _inherit = 'res.partner'

    arabic_name = fields.Char("Arabic Name")
    building_no = fields.Char('Building No')
    additional_no = fields.Char('P.O.Box')
    other_seller_id = fields.Char('Other Seller Id')
    journal_id = fields.Many2one('account.journal', string='Journal')


class ResCompany(models.Model):
    _inherit = 'res.company'

    building_no = fields.Char(related='partner_id.building_no', store=True, readonly=False, string='Building No')
    additional_no = fields.Char(related='partner_id.additional_no', store=True, readonly=False, string='Additional No')
    other_seller_id = fields.Char(related='partner_id.other_seller_id', store=True, readonly=False, string='Other Seller Id')
    arabic_name = fields.Char('Name')
    arabic_street = fields.Char('Street')
    arabic_street2 = fields.Char('Street2')
    arabic_city = fields.Char('City')
    arabic_state = fields.Char('State')
    arabic_country = fields.Char('Country')
    arabic_zip = fields.Char('Zip')


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def get_product_arabic_name(self,pid):
        translation = self.env['ir.translation'].search([
            ('name','=','product.product,name'),('state','=','translated'),
            ('res_id','=',pid)])
        if translation :
            return translation.value
        else: 
            product = self.env['product.product'].browse(int(pid))
            translation = self.env['ir.translation'].search([
                ('name','=','product.product,name'),('state','=','translated'),
                ('res_id','=',product.product_tmpl_id.id)])
            if translation :
                return translation.value
        return ''    

    @api.model
    def get_qr_code(self):
        data = 'Supplier Name : ' + str(self.company_id.name or '')
        data += '\nVAT Number : ' + str(self.company_id.vat or '')
        data += '\nDate Order : ' + str(self.date_order or '')
        data += '\nTotal VAT : ' + str(self.amount_tax or '')
        data += '\nTotal Amount : ' + str(self.currency_id and self.currency_id.symbol or '') + ' ' + str(self.amount_total or 0.0)
        img = qrcode.make(data)
        result = io.BytesIO()
        img.save(result, format='PNG')
        result.seek(0)
        img_bytes = result.read()
        base64_encoded_result_bytes = base64.b64encode(img_bytes)
        base64_encoded_result_str = base64_encoded_result_bytes.decode('ascii')
        return base64_encoded_result_str

    def amount_word(self, amount):
        language = self.partner_id.lang or 'en'
        language_id = self.env['res.lang'].search([('code', '=', 'ar_001')])
        if language_id:
            language = language_id.iso_code
        amount_str =  str('{:2f}'.format(amount))
        amount_str_splt = amount_str.split('.')
        before_point_value = amount_str_splt[0]
        after_point_value = amount_str_splt[1][:2]           
        before_amount_words = num2words(int(before_point_value),lang=language)
        after_amount_words = num2words(int(after_point_value),lang=language)
        amount = before_amount_words + ' ' + after_amount_words
        return amount

    def amount_total_words(self, amount):
        words_amount = self.company_id.currency_id.amount_to_text(amount)
        return words_amount


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    @api.model
    def _get_line_batch_key(self, line):
        ''' Turn the line passed as parameter to a dictionary defining on which way the lines
        will be grouped together.
        :return: A python dictionary.
        '''
        move = line.move_id

        partner_bank_account = self.env['res.partner.bank']
        if move.is_invoice(include_receipts=True):
            partner_bank_account = move.partner_bank_id._origin

        return {
            'partner_id': line.partner_id.id,
            'account_id': line.account_id.id,
            'currency_id': line.currency_id.id,
            'partner_bank_id': partner_bank_account.id,
            'partner_type': 'customer' if line.account_internal_type == 'receivable' else 'supplier',
            'payment_type': 'inbound' if line.balance > 0.0 else 'outbound',
            'journal_type': line.partner_id.journal_id
        }

    @api.depends('can_edit_wizard', 'company_id')
    def _compute_journal_id(self):
        for wizard in self:
            print(wizard, "wizard................................................//////////////////////////////////")
            if wizard.can_edit_wizard:
                batch = wizard._get_batches()[0]

                print(batch, "BATCCHHH.....................")
                # print(batch.get('key_values', {}).get('journal_type'),"BATCCHHH.....................")
                batches = batch.get('key_values', {}).get('journal_type')
                wizard.journal_id = batches
                print(wizard.journal_id, " wizard journal_id ")
                print(wizard.journal_id.name, " wizard journal_id  names.....................")

            else:
                wizard.journal_id = self.env['account.journal'].search([
                    ('type', 'in', ('bank', 'cash')),
                    ('company_id', '=', wizard.company_id.id),
                ], limit=1)


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def get_product_arabic_name(self,pid):
        translation = self.env['ir.translation'].search([
            ('name','=','product.product,name'),('state','=','translated'),
            ('res_id','=',pid)])
        if translation :
            return translation.value
        else: 
            product = self.env['product.product'].browse(int(pid))
            translation = self.env['ir.translation'].search([
                ('name','=','product.product,name'),('state','=','translated'),
                ('res_id','=',product.product_tmpl_id.id)])
            if translation :
                return translation.value
        return ''    

    @api.model
    def get_qr_code(self):
        data = 'Supplier Name : ' + str(self.company_id.name or '')
        data += '\nVAT Number : ' + str(self.company_id.vat or '')
        data += '\nDate Order : ' + str(self.date_order or '')
        data += '\nTotal VAT : ' + str(self.amount_tax or '')
        data += '\nTotal Amount : ' + str(self.currency_id and self.currency_id.symbol or '') + ' ' + str(self.amount_total or 0.0)      
        img = qrcode.make(data)
        result = io.BytesIO()
        img.save(result, format='PNG')
        result.seek(0)
        img_bytes = result.read()
        base64_encoded_result_bytes = base64.b64encode(img_bytes)
        base64_encoded_result_str = base64_encoded_result_bytes.decode('ascii')
        return base64_encoded_result_str

    def amount_word(self, amount):
        language = self.partner_id.lang or 'en'
        language_id = self.env['res.lang'].search([('code', '=', 'ar_001')])
        if language_id:
            language = language_id.iso_code
        amount_str =  str('{:2f}'.format(amount))
        amount_str_splt = amount_str.split('.')
        before_point_value = amount_str_splt[0]
        after_point_value = amount_str_splt[1][:2]           
        before_amount_words = num2words(int(before_point_value),lang=language)
        after_amount_words = num2words(int(after_point_value),lang=language)
        amount = before_amount_words + ' ' + after_amount_words
        return amount

    def amount_total_words(self, amount):
        words_amount = self.company_id.currency_id.amount_to_text(amount)
        return words_amount

class TermsAndConditionDescription(models.Model):
    _name = 'terms.description.desc'
    _rec_name = 'description'

    description = fields.Char(string="Description", tracking=True)
    terms_condition_id = fields.Many2one('sale.order', tracking=True)



class TermsConditionMaster(models.Model):
    _name = 'terms.condition.master'
    _rec_name = 'category_id'

    category_id = fields.Many2one('category.master', string="Category")
    line_ids = fields.One2many('terms.condition.line', 'specification_id', string="Specification Line")

class TermsConditionLine(models.Model):
    _name = 'terms.condition.line'
    _rec_name = 'name'

    specification_id = fields.Many2one('terms.condition.master', string="Description")
    name = fields.Char(string="Name", tracking=True)