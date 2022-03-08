# Copyright 2021 Criptomart <https://criptomart.net>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging

from odoo import api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)
 
class PosOrder(models.Model):
    _inherit = 'pos.order'

    def action_pos_order_paid(self):
        lines_membership = self.lines.filtered('product_id.membership')
        lines_dispense = self.lines.filtered(lambda line: line.product_id.membership == False)
        if lines_membership:
          _logger.warning("cuota detectada")
          current_session = self.env['pos.session'].search([('state', '!=', 'closed'), ('user_id', '=', self.env.uid)], limit=1)
          amount_membership = sum(lines_membership.mapped(lambda r: r.price_subtotal))
          amount_dispense = sum(lines_dispense.mapped(lambda r: r.price_subtotal))
          _logger.warning("amount cuota : %s -- amount aport : %s" %(amount_membership, amount_dispense))
          if amount_dispense:
              _logger.warning("cuota + aportacion detectada")
              # dividimos el pago
              old_pay = self.statement_ids
              new_pay = old_pay.copy({'amount': amount_membership})
              old_pay.write({'amount': amount_dispense })
              # creamos nueva sale order
              clone = self.create({
                    'partner_id': self.partner_id.id,
                    'name': self.name + ' SPLIT',
                    'session_id': current_session.id,
                    'date_order': fields.Datetime.now(),
                    'pos_reference': self.pos_reference + '_cuota', 
                    'lines': [],
                    'amount_tax': self.amount_tax,
                    'amount_total': amount_membership,
                    'amount_paid': amount_membership,
                    'amount_return': 0,
                    'invoice_group': True,
                    'statement_ids': [ new_pay ],
                    'pricelist_id': self.pricelist_id.id
              })
              for line in lines_membership:
                clone_line = {
                    'name': line.name + ' CUOTA',
                    'order_id': clone.id,
                    'qty': line.qty,
                    'price_subtotal': line.price_subtotal,
                    'price_subtotal_incl': line.price_subtotal_incl,
                    'product_id': line.product_id.id                    
                }
                _logger.warning("clone line : %s" %clone_line)
                clone.lines = [(0, 0, clone_line)]
                self.lines = [(2, line.id, 0)]
              
              clone.action_pos_order_invoice()
              clone.invoice_id.sudo().action_invoice_open()
              clone.invoice_id.sudo().action_invoice_paid()
          else:
              _logger.warning("solo cuota, creando factura")
              self.to_invoice = True 
              self.action_pos_order_invoice()
              self.invoice_id.sudo().action_invoice_open()
              self.account_move = self.invoice_id.move_id
              #self.env['pos.order']._match_payment_to_invoice(self) 
              #self.invoice_id.sudo().action_invoice_paid()
              
        return super(PosOrder, self).action_pos_order_paid()
        

