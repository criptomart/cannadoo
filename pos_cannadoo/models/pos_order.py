from odoo import _, api, fields, models, tools


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    product_list_price = fields.Float(
        string="Precio de dispensa",
        readonly=True,
        compute="_compute_list_price",
        store=True,
    )

    @api.multi
    def _compute_list_price(self):
        for line in self:
            line.product_list_price = line.product_id.list_price
