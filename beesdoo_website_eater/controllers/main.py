# -*- coding: utf-8 -*-

# Copyright 2015-2016 Odoo S.A.
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# Copyright 2018 Rémy Taymans <remytaymans@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from openerp.http import request

from openerp.addons.website_portal_v10.controllers.main import WebsiteAccount


class EaterWebsiteAccount(WebsiteAccount):

    def _prepare_portal_layout_values(self):
        values = super(EaterWebsiteAccount,
                       self)._prepare_portal_layout_values()
        partner = request.env.user.partner_id.commercial_partner_id
        values.update({
            'eaters': partner.child_eater_ids,
        })
        return values
