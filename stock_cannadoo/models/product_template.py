import logging

from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    def _get_default_uom_id_gram(self):
        return self.env["uom.uom"].search([('name','=','g')], limit=1, order='id').id

    type = fields.Selection(default='product')
            
    uom_id = fields.Many2one(
        'uom.uom', 'Unit of Measure',
        default=_get_default_uom_id_gram, required=True,
        help="Default unit of measure used for all stock operations.")        
        
    uom_po_id = fields.Many2one(
        'uom.uom', 'Purchase Unit of Measure',
        default=_get_default_uom_id_gram, required=True,
        help="Default unit of measure used for purchase orders. It must be in the same category as the default unit of measure.")
