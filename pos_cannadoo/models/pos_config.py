from odoo import fields, models


class PosDiscountMode(models.Model):
    _inherit = "pos.config"

    discount_mode = fields.Boolean(
        string="Quantity discount enabled",
        help="Change the regular Odoo discount mode, set up the quantity and recalculate product price.",
    )
    default_pos_price = fields.Float(
        string="Default order line price",
        help="Default order line price when adding products in grams in PoS.",
        default=10,
    )
