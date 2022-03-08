from odoo import fields, models

class StockScrap(models.Model):
   _name = 'stock.scrap'
   _inherit = ['stock.scrap','mail.thread']
   _description = 'Chatter for scrap form'
