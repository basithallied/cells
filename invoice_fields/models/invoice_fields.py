from odoo import api, fields, models, SUPERUSER_ID, _
from collections import defaultdict
# from odoo.osv import expression

class AccountMoving(models.Model):
    _inherit = "account.move"

    def invoice_button(self):
        # def invoice_button(self):
        #     print(self.bank_id.id, "bank id")
        #     print(self.bank_id.name, "bank id")
        #     print(self.bank_id.acc_no, "acc no")
        #     print(self.bank_id.acc_no[-4:], "last digits")
        #     # self.bank_id[-4:] = self.bank_id.name + self.bank_id.acc_no[-4:]
        #     word = '*'.join(self.bank_id[-4:])
        #
        #     print(word,"@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            # return self.env.ref('e_tax_invoice_saudi_aio.action_report_tax_invoice').report_action(self)

            return self.env.ref('e_tax_invoice_saudi_aio.action_report_tax_invoice').report_action(self)

    bank_id = fields.Many2one('res.bank', string='Bank')
    conversion_rates_new = fields.Many2one('create.con', string='Conversion To')
    rate_confirm = fields.Char(string="Rate")
    job_ref = fields.Char(string='Job Reference')

    # def onchange_acc_no(self, cr, uid, ids,  context=None):
    #     v = {}
    #     if self.bank_id and self.acc_no:
    #         v['name'] = self.bank_id + self.acc_no
    #     return {'value': v}

    # # @api.depends('bank_id', 'acc_no')
    # def name_get(self):
    #     print("@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    #     result = []
    #     for rec in self:
    #         rec.bank_id = rec.bank_id + rec.acc_no
    #         print(rec.acc_no)
    #         result.append((rec.id, rec.bank_id ))
    #     return result
        # last_digit = self.bank_id.acc_no[-4:]
        # for bank_id in self:
        #     print(bank_id,"BANK ID -------------------------------------------")
        #     name = bank_id.name + (bank_id and (' - ' + last_digit) or '')
        #     result.append((bank_id.id, name))
        # return result

    # @api.model
    # def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
    #     args = args or []
    #     domain = []
    #     if name:
    #         domain = ['|', ('bic', '=ilike', name + '%'), ('name', operator, name)]
    #         if operator in expression.NEGATIVE_TERM_OPERATORS:
    #             domain = ['&'] + domain
    #     return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)

    # def _my_methode(self, cr, uid, ids, bank_id, arg, context=None):
    #
    #     record = self.env['account.move'].search([('bank_id', '=', self.bank_id)], limit=1)
    #     print(record,"RECORD>>>>>>>")
        # records = self.browse(cr, uid, ids)
        # # result = dict((x, '') for x in ids)
        # for r in records:
        #     print(r, "RECCCCCCC")
        #     if (r.bank_id and r.bank_id.acc_no[-4:]):
        #         result[r.id] = "%s %s" % \
        #         (r.bank_id or '', r.bank_id.acc_no[-4:] or '')
        # return result


        # res = []
        # for record in self:
        #     name = record.name
        #     if record.insurance_percentage:
        #         name = '[' + record.insurance_percentage + ']' + name
        #     res.append((record.id, name))


    # def onchange_first_last(self, acc_no, bank_id, context=None):
    #     v = {}
    #     if bank_id and acc_no:
    #         v['name'] = first_name + last_name
    #     return {'value': v}



    # def create(self, bank_id, context=None):

    # self.bank_id[:12] = self.bank_id.name + self.bank_id.acc_no[-4:]

    # extension = str(self.bank_id.name or '') + ' ' + str(self.bank_id.acc_no[-4:] or '')
    # print(extension, "BANK NAME")
    # vals['name'] = name
    # return super(sample_model, self).create(cr, uid, vals, context=context)

    @api.onchange('conversion_rates_new')
    def _onchange_rate_swap(self):
        self.rate_confirm = self.conversion_rates_new.con_rate

    @api.onchange('rate_confirm')
    def _onchange_exchange_value(self):
        self.conversion_rates_new.con_rate =  self.rate_confirm


class CreateCon(models.Model):
    _name = "create.con"
    _description = "conversion rate"

    name = fields.Char(string="name")
    con_rate = fields.Float(string="Rate")


    # @api.model
    # def _get_default_currency(self):
    #     ''' Get the default currency from either the journal, either the default journal's company. '''
    #     journal = self._get_default_journal()
    #     return journal.currency_id or journal.company_id.currency_id
    #
    #
    # @api.depends('invoice_line_ids.discount')
    # def _compute_amount_after(self):
    #     for move in self:
    #         con_discount_total = 0.0
    #         for line in move.invoice_line_ids:
    #             con_discount_total += round(((line.price_unit * line.quantity) - line.price_subtotal), 2)
    #             self.con_discount_total = con_discount_total
    #             print("\\\\\\\\\\", con_discount_total)
    #
    # # @api.depends('invoice_line_ids.untaxed_amount')
    # # def _compute_amount_excl(self):
    # #     # self.con_total_ex_vat = self.amount_untaxed + self.con_discount_total
    # #     print("]]]]]]]]]]]")
    #
    # @api.depends('currency_id')
    # def _compute_amount_final(self):
    #     if self.currency_id == 'SAR':
    #         usd = self.env['res.currency'].search([('name', '=', 'USD')])
    #         print("----------", usd)
    #
    #
    # currency_id = fields.Many2one('res.currency', store=True, readonly=True, tracking=True, required=True, states={'draft': [('readonly', False)]},
    #                                   string='Currency',default=_get_default_currency, compute='_compute_amount_final')
    # # con_total_ex_vat = fields.Char(string="Total Excluding Vat", store=True, readonly=True, compute='_compute_amount_excl')
    # con_discount_total = fields.Char(string="Total Discount", store=True, readonly=True, compute='_compute_amount_after')



    # @api.onchange('currency_id')
    # def onchange_currency_id(self):
    #     store = self.currency_id
    #     print("/////////////", store)
    #     usd = self.env['res.currency'].search([('name', '=', 'USD')])
        # eur = self.env['res.currency'].search([('name', '=', 'EUR')])
        # sar = self.env['res.currency'].search([('name', '=', 'SAR')])
        # print("@@@@@@@@@@@@@@", usd.rate)
        # print("!!!!!!!!!!!!!!!", eur.rate)
        # print("!!!!!!!!!!!!!!!", sar.rate)

        # print("///////////", self.currency_id.name)


