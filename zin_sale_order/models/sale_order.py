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

    pad_id = fields.Many2one("product.product", "Pad")
    pad_qty = fields.Float("Pad Qty")
    is_maintenance = fields.Boolean("Maintenance")


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    pad_id = fields.Many2one("product.product", "Pad")
    pad_qty = fields.Float("Pad Qty")
