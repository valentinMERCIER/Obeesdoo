# -*- coding: utf-8 -*-

# Copyright 2017-2018 Rémy Taymans <remytaymans@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from openerp import fields, models, http
from openerp.http import request

from website_portal_v10.controllers.main import WebsiteAccount


class FormController(WebsiteAccount):

    @http.route(['/my/account'], type='http', auth='user', website=True)
    def details(self, redirect=None, **post):
        partner = request.env['res.users'].browse(request.uid).partner_id
        values = {
            'error': {},
            'error_message': []
        }

        if post:
            values.update(post)
            if not error:
                post.update({'zip': post.pop('zipcode', '')})
                if partner.type == "contact":
                    address_fields = {
                        'city': post.pop('city'),
                        'street': post.pop('street'),
                        'street2': post.pop('street2'),
                        'zip': post.pop('zip'),
                        'country_id': post.pop('country_id'),
                        'state_id': post.pop('state_id')
                    }
                    partner.commercial_partner_id.sudo().write(address_fields)
                partner.sudo().write(post)
                if redirect:
                    return request.redirect(redirect)
                return request.redirect('/my/home')

        countries = request.env['res.country'].sudo().search([])
        states = request.env['res.country.state'].sudo().search([])

        values.update({
            'partner': partner,
            'countries': countries,
            'states': states,
            'has_check_vat': hasattr(request.env['res.partner'], 'check_vat'),
            'redirect': redirect,
        })

        return request.website.render("website_portal.details", values)
