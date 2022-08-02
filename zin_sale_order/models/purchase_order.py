from odoo import api, fields, models, SUPERUSER_ID, _


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    container_qty = fields.Float("Container Qty")
    total_amount = fields.Float("Total Amount")
    received_qty = fields.Float("Received Qty")
    remaining_qty = fields.Float("Remaining Qty")
    bill_landing_no = fields.Char("Bill Of Landing Number")
    shipping_company_id = fields.Many2one('res.partner', "Shipping Company")
    shipping_date = fields.Date("Shipping Date")
    expected_date = fields.Date("Expected Date")
    port = fields.Char("Port")
    arrival_date_riyadh = fields.Date("Arrival Date Riyadh")
    update_check_for_eta = fields.Boolean("Update Check For ETA")
    original_documents = fields.Binary("Original Documents")
    copy_documents = fields.Binary("Copy Documents")
    saber_certificate = fields.Binary("Saber certificate")
    shipping_status = fields.Selection([
        ('draft', 'Draft'),
        ('transit', 'Transit'),
        ('arrived', 'Arrived')], string="Shipping Status", default='draft', required=True)
    tracking_link = fields.Text(string='Tracking Link')
    tracking_notes = fields.Text(string='Notes')

