from odoo import api, fields, models, SUPERUSER_ID, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model_create_multi
    def create(self, vals):
        if vals[0]['is_maintenance']:
            seq = self.env['ir.sequence'].next_by_code('maintenance_order') or _('New')
            vals[0]['name'] = seq
        result = super(SaleOrder, self).create(vals)
        return result

    # pad_id = fields.Many2one("product.product", "Pad")
    # pad_qty = fields.Float("Pad Qty")
    is_maintenance = fields.Boolean("Maintenance")
    category_ids = fields.Many2one('category.master', string="Category", tracking=True)
    terms_condition_ids = fields.One2many('terms.description.desc', 'terms_condition_id',
                                       string="Terms and Conditions", tracking=True)


    @api.onchange('category_ids')
    def onchange_update_description(self):
        if self.category_ids:
            self.terms_condition_ids = False
            category_list = []
            for category in self.category_ids:
                category_list.append(category.id)
            spec = self.env['terms.condition.master'].search([('category_id', 'in', category_list)])
            vals = []
            for val in spec:
                spec_line = self.env['terms.condition.line'].search([('specification_id', '=', val.id)])
                for val in spec_line:
                    vals.append((0, 0, {'description': val.name}))
            self.terms_condition_ids = vals



# merlin added
class TermsAndConditionDescription(models.Model):
    _name = 'terms.description.desc'
    _rec_name = 'description'

    description = fields.Char(string="Description", tracking=True)
    terms_condition_id = fields.Many2one('sale.order', tracking=True)


class CategoryMaster(models.Model):
    _name = 'category.master'

    name = fields.Char(string="Category", tracking=True)

class TermsConditionMaster(models.Model):
    _name = 'terms.condition.master'
    _rec_name = 'category_id'

    category_id = fields.Many2one('category.master', string="Category")
    line_ids = fields.One2many('terms.condition.line','specification_id', string="Specification Line")


class TermsConditionLine(models.Model):
    _name = 'terms.condition.line'
    _rec_name = 'name'

    specification_id = fields.Many2one('terms.condition.master', string="Description")
    name = fields.Char(string="Name", tracking=True)



class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    pad_id = fields.Many2one("product.product", "Pad")
    pad_qty = fields.Float("Pad Qty")
    print(pad_qty,'zzzz')

# commented
# new function added
#     @api.onchange('order_line')
#     def _prepare_invoice_line(self):
#         res = super(SaleOrderLine, self)._prepare_invoice_line()
#         res.update({
#             'description ': self.description
#         })
#         return res

# ////////////

