from odoo import api, fields, models, SUPERUSER_ID, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    cooler_term_id = fields.Many2one("cells.terms.conditions", string='Cooler Terms',
                                     config_parameter="zin_sale_order.cooler_term_id")
    pad_term_id = fields.Many2one("cells.terms.conditions", string='Cooling Pad Terms',
                                  config_parameter="zin_sale_order.pad_term_id")
