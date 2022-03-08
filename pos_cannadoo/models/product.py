from odoo import _, api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    available_in_pos = fields.Boolean(
        string="Available in POS",
        help="Check if you want this product to appear in the Point of Sale.",
        default=True,
    )
    pos_categ_id = fields.Many2one(
        "pos.category",
        string="Point of Sale Category",
        help="Category used in the Point of Sale.",
    )
