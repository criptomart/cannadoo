# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from odoo import api, fields, models
_logger = logging.getLogger(__name__)
try:
    from odoo.addons.membership.models.membership import STATE
except ImportError:
    _logger.warning("Cannot import 'membership' addon.")
    _logger.debug("Details", exc_info=True)


class ResPartner(models.Model):
    _inherit = "res.partner"

    image_id = fields.Binary("Imagen ID Front", attachment=True,
        help="This field holds the image of the ID card for this contact",)

    image_id_back = fields.Binary("Imagen ID Back", attachment=True,
        help="This field holds the image of the ID card for this contact",)
