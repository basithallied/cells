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

    specification_id = fields.Many2one('terms.condition.master', string="Specification")
    name = fields.Char(string="Name", tracking=True)





class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    pad_id = fields.Many2one("product.product", "Pad")
    pad_qty = fields.Float("Pad Qty")
