# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import api, fields, models

# Sale Terms And Conditions


class SaleInherate(models.Model):
    _inherit = 'sale.order'

    term_conditions = fields.Many2one(
        'sh.so.tnc', string="Terms And Conditions")
    terms_detail = fields.Html(string="Conditions Detail")
    sh_in_report = fields.Boolean('Display in Report ??', default=True)
    
    def _prepare_invoice(self):
        
        invoice_vals = super(SaleInherate, self)._prepare_invoice()
        invoice_vals['term_conditions'] = self.term_conditions.id
        invoice_vals['terms_detail'] = self.terms_detail
        
        return invoice_vals

    @api.onchange('term_conditions')
    def _onchange_term_con(self):
        if self.sale_order_template_id:
            if self.sale_order_template_id.term_conditions == self.term_conditions:
                self.terms_detail = self.sale_order_template_id.terms_detail
            else:
                self.terms_detail = self.term_conditions.terms_con

        elif self.term_conditions:
            self.terms_detail = self.term_conditions.terms_con

    @api.onchange('sale_order_template_id')
    def _onchange_sale_order_template_id(self):
        if self.sale_order_template_id:
            self.term_conditions = self.sale_order_template_id.term_conditions
            self.terms_detail = self.sale_order_template_id.terms_detail
            
class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _prepare_invoice_values(self, order, name, amount, so_line):
        
        invoice_vals = super(SaleAdvancePaymentInv, self)._prepare_invoice_values(order, name, amount, so_line)
        invoice_vals['term_conditions'] = order.term_conditions.id
        invoice_vals['terms_detail'] = order.terms_detail
        return invoice_vals

class SaleOrderTemplate(models.Model):
    _inherit = 'sale.order.template'

    term_conditions = fields.Many2one(
        'sh.so.tnc', string="Terms And Conditions")
    terms_detail = fields.Html(string="Conditions Detail")

    @api.onchange('term_conditions')
    def _onchange_term_con(self):
        if self.term_conditions:
            self.terms_detail = self.term_conditions.terms_con
