# Copyright 2004-2009 Tiny SPRL (<http://tiny.be>).
# Copyright 2013 initOS GmbH & Co. KG (<http://www.initos.com>).
# Copyright 2016 Tecnativa - Vicent Cubells
# Copyright 2016 Camptocamp - Akim Juillerat (<http://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import api, fields, models, exceptions, _

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    """Assigns 'ref' from a sequence on creation and copying"""
    _inherit = 'res.partner'

    code_number = fields.Integer("Número de código miembro")

    @api.multi
    def _get_next_ref(self, vals=None):
        if not vals and not self:  # pragma: no cover
            raise exceptions.UserError(_(
                'Either field values or an id must be provided.'))
        if vals and 'name' in vals:  
            name = vals['name'].split()
        else:
            name = self.name.split()
        _logger.debug("get_next_ref for : %s" %name)
        if len(name) < 2:
            raise exceptions.UserError(_(
                'Se requiere nombre y un apellido al menos.'))
        
        id = str(name[0][0] + name[1][0]).upper()
        # Search active and inactive partners
        last_id = self.env['res.partner'].with_context(active_test=False).search([('ref','like',id )], limit=1, order="code_number desc")
        last_num = 1
        if last_id:
            last_num += int(last_id.ref[2:])
        id += str(last_num)
        return id

    @api.model
    def _compute_code_number(self, vals):
        code_number = vals.get('ref')[2:]
        return int(code_number)

    @api.model
    def cron_compute_code_number(self):
        partners = self.env['res.partner'].with_context(active_test=False).search([])
        for record in partners:
            if record.ref:
                record.code_number = int(record.ref[2:])

    @api.model
    def create(self, vals):
        if not vals.get('ref') and self._needsRef(vals=vals):
            vals['ref'] = self._get_next_ref(vals=vals)
            vals['code_number'] = self._compute_code_number(vals)
        return super(ResPartner, self).create(vals)

    @api.multi
    def copy(self, default=None):
        default = default or {}
        if self._needsRef():
            default['ref'] = self._get_next_ref()
            default['code_number'] = self._compute_code_number(default)            
        return super(ResPartner, self).copy(default)

    @api.multi
    def write(self, vals):
        for partner in self:
            partner_vals = vals.copy()
            if (
                    not partner_vals.get('ref')
                    and partner._needsRef(partner_vals)
                    and not partner.ref
            ):
                partner_vals['ref'] = partner._get_next_ref(vals=partner_vals)
                partner_vals['code_number'] = self._compute_code_number(partner_vals)                
            super(ResPartner, partner).write(partner_vals)
        return True

    @api.multi
    def _needsRef(self, vals=None):
        """
        Checks whether a sequence value should be assigned to a partner's 'ref'

        :param vals: known field values of the partner object
        :return: true iff a sequence value should be assigned to the\
                      partner's 'ref'
        """
        if not vals and not self:  # pragma: no cover
            raise exceptions.UserError(_(
                'Either field values or an id must be provided.'))
        # only assign a 'ref' to commercial partners and customers
        if self:
            vals = {}
            vals['is_company'] = self.is_company
            vals['parent_id'] = self.parent_id
            vals['customer'] = self.customer            
        return vals.get('is_company') or not vals.get('parent_id') and vals.get('customer')

    @api.model
    def _commercial_fields(self):
        """
        Make the partner reference a field that is propagated
        to the partner's contacts
        """
        return super(ResPartner, self)._commercial_fields() + ['ref']

class Users(models.Model):
    _inherit = 'res.users'

    @api.model_create_multi
    def create(self, vals_list):
        users = super(Users, self.with_context(default_customer=False)).create(vals_list)
        for user in users:
            user.partner_id.email = user.login
        return users
