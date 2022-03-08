# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

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

    membership_category_id = fields.Many2one(
        string="Membership Category",
        readonly=False,
        store=True,
        comodel_name="membership.membership_category",
    )

    property_product_pricelist = fields.Many2one(
        comodel_name="product.pricelist",
        string="Membership pricelist",
        related="membership_category_id.pricelist",
        readonly=True,
        store=True,
    )

    last_order_date = fields.Datetime(
        string="Last order date",
        readonly=True,
        store=True,
        compute="_compute_last_order_date",
    )

    def _compute_last_order_date(self):
        for record in self:
            last_confirmed_order = self.env["pos.order"].search(
                [("partner_id", "=", record.id)], order="date_order desc", limit=1
            )
            record["last_order_date"] = last_confirmed_order.date_order

    @api.onchange("vat")
    def set_upper(self):
        if self.vat:
            self.vat = str(self.vat).upper()
        else:
            self.vat = ""
        return
