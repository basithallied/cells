from odoo import api, fields, models, SUPERUSER_ID, _

READONLY_STATES = {
        'purchase': [('readonly', True)],
        'done': [('readonly', True)],
        'cancel': [('readonly', True)],
    }


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
    arrival_date_riyadh = fields.Date("Arrival Date")
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
    date_planned = fields.Datetime(tracking=True,
        string='Receipt Date', index=True, copy=False, compute='_compute_date_planned', store=True, readonly=False,
        help="Delivery date promised by vendor. This date is used to determine expected arrival of products.")
    purchase_picking_policy = fields.Selection([
        ('direct', 'As soon as possible'),
        ('one', 'When all products are ready')],
        string='Shipping Policy', required=True, readonly=True, default='direct',
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}
        , help="If you deliver all products at once, the delivery order will be scheduled based on the greatest "
               "product lead time. Otherwise, it will be based on the shortest.")
    customer_so = fields.Char('Customer SO')
    purchase_ship_to_city = fields.Char('Ship To City')

