  # -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import Website

import logging
_logger = logging.getLogger(__name__)

class PartnerForm(http.Controller):
    #mention class name
    @http.route(['/member/form'], type='http', auth="user", website=True)
    #mention the authentication to be either public or user.
    def partner_form(self, **post):
        return request.render("web_search_member.tmp_customer_form", {})

    @http.route(['/member/form/submit'], type='http', auth="public", website=True)
    def customer_form_submit(self, **post):
        # Get members
        name_search = post.get('name')
        id_search = post.get('id')
        ref_search = post.get('ref')
        
        if id_search:
            member = (
                request.env["res.partner"]
                .sudo()
                .search([("vat", "=", id_search.upper())])
            )
        elif ref_search:
            member = (
                request.env["res.partner"]
                .sudo()
                .search([("ref", "=", ref_search.upper())])
            )
        elif name_search:
            member = (
                request.env["res.partner"]
                .sudo()
                .search([("name", "=", name_search)])
            )            
        
        _logger.debug("search member: %s" % member)
        if member:
            vals = {
                'partner': member,
            }
        else:
            vals = {
                'not_found': True,
            }
        return request.render("web_search_member.tmp_customer_form", vals)
        
class Website(Website):

    @http.route(website=True, auth="public")
    def web_login(self, redirect=None, *args, **kw):
        response = super(Website, self).web_login(redirect=redirect, *args, **kw)
        if not redirect and request.params['login_success']:
            if request.env['res.users'].browse(request.uid).has_group('base.group_user'):
                redirect = b'/web?' + request.httprequest.query_string
            else:
                redirect = '/member/form'
            return http.redirect_with_hash(redirect)
        return response
