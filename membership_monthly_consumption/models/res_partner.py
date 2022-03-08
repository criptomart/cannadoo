# Copyright 2021 CriptoMart <tech@criptomart.net>
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

    monthly_consumption_limit = fields.Float("Monthly Consumption", 
        help="Configure the limit for the monthly consumption of this member.",
        default=90.0)

    monthly_consumption_current = fields.Float("Current Month", 
        readonly=True, help="This field shows the consumption of the member in the current month.",)
        
    @api.model
    def cron_reset_month_consumption(self):
        _logger.info("[CRON] Reset members month consumption")
        partner_ids = self.env['res.partner'].search([])
        members_with_consum_ids = partner_ids.filtered(lambda l: l.monthly_consumption_current > 0)
        _logger.info("[CRON] members with month consumption: %s" % len(members_with_consum_ids))
        for member in members_with_consum_ids:
            member.monthly_consumption_current = 0
