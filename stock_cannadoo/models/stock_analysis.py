from odoo import tools
from odoo import models, fields, api


class StockAnalysis(models.Model):
    _inherit = 'stock.analysis'

    product_list_price = fields.Float(string='Price', readonly=True, compute='_compute_product_price', store=True)
    
    @api.multi
    def _compute_product_price(self):
        for product in self:
            product.product_list_price = product.product_id.price_list
            
    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            """CREATE or REPLACE VIEW %s as (
            SELECT
                quant.id AS id,
                quant.product_id AS product_id,
                quant.location_id AS location_id,
                quant.quantity AS quantity,
                quant.lot_id AS lot_id,
                quant.package_id AS package_id,
                quant.in_date AS in_date,
                quant.company_id,
                template.list_price AS product_list_price,
                template.categ_id AS categ_id
            FROM stock_quant AS quant
            JOIN product_product prod ON prod.id = quant.product_id
            JOIN product_template template
                ON template.id = prod.product_tmpl_id
            )"""
            % (self._table)
        )    
