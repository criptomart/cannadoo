import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)
try:
    from odoo.addons.membership.models.membership import STATE
except ImportError:
    _logger.warning("Cannot import 'membership' addon.")
    _logger.debug("Details", exc_info=True)


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def create_from_ui(self, partner):
        # FIX!! Not working
        #        _logger.debug("create from ui, add pricelist")
        #        if partner.get('membership_category_id'):
        #            category = self.env['membership.membership_category'].browse([int(partner.get('membership_category_id'))])
        #            _logger.debug("category: %s" % category)
        #            pricelist = category.pricelist
        #            _logger.debug("pricelist: %s" % pricelist)
        #            if category:
        #                partner['property_product_pricelist'] = str(pricelist.id)
        #                _logger.debug("partner: %s" % partner)
        partner_id = partner["id"]
        if not partner_id:  # New partner
            _logger.debug("New partner, asign code")
            partner["ref"] = self._get_next_ref(vals=partner)
            partner["code_number"] = self._compute_code_number(partner)
        return super(ResPartner, self).create_from_ui(partner)
