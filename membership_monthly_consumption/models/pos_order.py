# Copyright 2021 Criptomart <https://criptomart.net>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging

from odoo import api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)
 
class PosOrder(models.Model):
    _inherit = 'pos.order'

    def action_pos_order_paid(self):
        lines_uom_gram = self.lines.filtered(lambda line: line.product_id.uom_id.category_id.measure_type == 'weight')
        if lines_uom_gram:
          for line in lines_uom_gram:
            self.partner_id.monthly_consumption_current += line.qty
        return super(PosOrder, self).action_pos_order_paid()
