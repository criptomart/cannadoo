from odoo import fields, models


class PosOrderReport(models.Model):
    _inherit = "report.pos.order"

    # Overwrite to change integer for floats. Show decimals in report
    product_qty = fields.Float(string="Product Quantity", readonly=True)

    # New fields for grouping by price with and w/o discount
    price_unit = fields.Float(string="Unit Price", readonly=True)
    product_list_price = fields.Float(string="Precio de dispensa", readonly=True)

    # Add price_unit and product_price_list
    def _select(self):
        res = super()._select()
        res += ",l.price_unit AS price_unit,l.product_list_price AS product_list_price"
        return res

    def _group_by(self):
        res = super()._group_by()
        res += ",l.price_unit, l.product_list_price"
        return res
