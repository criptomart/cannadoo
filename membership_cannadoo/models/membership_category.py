# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)
try:
    from odoo.addons.membership.models.membership import STATE
except ImportError:
    _logger.warning("Cannot import 'membership' addon.")
    _logger.debug("Details", exc_info=True)


class MembershipCategory(models.Model):
    _inherit = "membership.membership_category"

    pricelist = fields.Many2one("product.pricelist", "Pricelist for category")
