# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from openerp.exceptions import UserError

class TaskType(models.TransientModel):
    _name = 'beesdoo.shift.welcome'

    _inherit = ['barcodes.barcode_events_mixin']

    partner_id = fields.Many2one('res.partner', string="Cooperator")
    message = fields.Html("Message")
    can_shop = fields.Boolean(related='partner_id.can_shop', readonly=True)

    def on_barcode_scanned(self, barcode):
        self._barcode_scanned = ''
        self.message = ''

        if barcode.startswith('42'):
            barcode = '0' + barcode
        if not barcode.startswith('042'):
            self.message = 'invalid barcode'
            return
        #0 at the begining of the code bar seems not to be scanned
        partner_ids = self.env['res.partner'].search([('barcode', '=', barcode)])
        if not partner_ids:
            self.message = "Member does not exist"
        elif len(partner_ids) > 1:
            self.message = "more then one member found with this barcode"
        else:
            self.partner_id = partner_ids[0]

    @api.onchange('partner_id')
    def _onchange_partner(self):
        values = {
            'rec': self
        }
        html_res = self.env.ref("beesdoo_shift_welcome_screen.welcome_message").render(values)
        self.message = html_res