/**
    Copyright (C) 2021: Criptomart (https://criptomart.net)
    @author: Criptomart (https://criptomart.net)
    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
*/

odoo.define('pos_cannadoo.models', function (require) {
    "use strict";

    var field_utils = require('web.field_utils');
    var utils = require('web.utils');
    var models = require('point_of_sale.models');
    var orderline_super = models.Orderline.prototype;
    var round_di = utils.round_decimals;
    var round_pr = utils.round_precision;

    models.NumpadState = models.NumpadState.extend({

    defaults: {
        buffer: 0,
        mode: "price"
    },

    reset: function() {
        this.set({
            buffer: "0",
            mode: this.defaults.mode
        });
    },

   });

    var order_super = models.Order.prototype;

    models.Order = models.Order.extend({

    fix_tax_included_price: function(line){
//        console.log("fix_tax");
    },
  
    select_orderline: function(line){
      order_super.select_orderline.apply(this, arguments);
        if (line && line.pos.gui.current_screen) {     
         var state = line.pos.gui.current_screen.numpad.state;
         if (line.product.uom_id[1] == "g") {
           state.changeMode('price');
           state.defaults.mode = 'price';
         } else {
           state.changeMode('quantity');
           state.defaults.mode = 'quantity';
         }
         line.pos.gui.current_screen.numpad.do_notify();
        }
    },

    });

    var orderline_id = 1;
    var orderline_super = models.Orderline.prototype;

    models.Orderline = models.Orderline.extend({

    initialize: function(attr, options){
        this.pos   = options.pos;
        this.order = options.order;
        if (options.json) {
            this.init_from_JSON(options.json);
            return;
        }
        this.product = options.product;
        this.set_product_lot(this.product);
        this.discount = 0;
        this.discountStr = '0';
        this.type = 'unit';
        this.selected = false;
        this.id = orderline_id++;
        this.price_manually_set = false;
        var price = this.product.get_price(this.order.pricelist, this.get_quantity());
        if (options.price) {
              this.price = round_di(parseFloat(options.price) || 0, this.pos.dp['Product Price']);
          } else {
              this.price = price;
          }
        if (this.product.uom_id[1] === "g") {
          this.set_quantity(this.pos.config.default_pos_price / price, 'do not recompute price');
          this.set_unit_price(this.pos.config.default_pos_price);
 
       } else {
          this.set_quantity(1, 'do not recompute price');
        }   
    },

    init_from_JSON: function(json) {
        this.product = this.pos.db.get_product_by_id(json.product_id);
        if (!this.product) {
            console.error('ERROR: attempting to recover product ID', json.product_id,
                'not available in the point of sale. Correct the product or clean the browser cache.');
        }
        this.set_product_lot(this.product);
        this.price = this.product.get_price(this.order.pricelist, this.get_quantity());
        this.discount = 0;
        this.discountStr = '0';
        this.id = json.id;
        orderline_id = Math.max(this.id+1,orderline_id);
        var pack_lot_lines = json.pack_lot_ids;
        for (var i = 0; i < pack_lot_lines.length; i++) {
            var packlotline = pack_lot_lines[i][2];
            var pack_lot_line = new exports.Packlotline({}, {'json': _.extend(packlotline, {'order_line':this})});
            this.pack_lot_lines.add(pack_lot_line);
        }
        this.set_unit_price(json.price_subtotal);
        this.set_quantity(json.qty);
        this.price_subtotal = json.price_subtotal;
        this.price_subtotal_incl = json.price_subtotal_incl;
        this.price_manually_set = false;
    },


    set_quantity: function(quantity, keep_price){
        this.order.assert_editable();
        if(quantity === 'remove'){
            this.order.remove_orderline(this);
            return;
        }else{
            var quant = parseFloat(quantity) || 0;
            var unit = this.get_unit();
            if(unit){
                if (unit.rounding) {
                    //var decimals = this.pos.dp['Product Unit of Measure'];
                    //var rounding = Math.max(unit.rounding, Math.pow(10, -decimals));
                    //console.log("decimals : " + decimals + " -- rounding : " + rounding);
                    this.quantity    = round_pr(quant, 0.00001);
                    this.quantityStr = field_utils.format.float(this.quantity, {digits: [69, 4]});
                } else {
                    this.quantity    = round_pr(quant, 1);
                    this.quantityStr = this.quantity.toFixed(0);
                }
            }else{
                this.quantity    = quant;
                this.quantityStr = '' + this.quantity;
            }
        }
        if(! keep_price && ! this.price_manually_set){
            this.price = this.product.get_price(this.order.pricelist, this.get_quantity());
            //this.order.fix_tax_included_price(this);
        }

        this.trigger('change', this);
    },

    set_discount: function (discount) {
        if (discount > 0) {
          if(this.pos.config.discount_mode) {
            this.order.assert_editable();
            var total = this.get_base_price();
            this.quantity    = round_pr(discount, 0.0001);
            this.quantityStr = field_utils.format.float(this.quantity, {digits: [69, 4]});
            this.price = total / discount;              
            this.trigger('change',this);
          } else {
            orderline_super.set_discount.apply(this, arguments);
          }
        }
    },

    set_unit_price: function(price){
        this.order.assert_editable();
        this.price = this.product.get_price(this.order.pricelist, this.get_quantity());
        if (this.product.uom_id[1] === "g") {   
            var quan = price / this.price;
            this.quantity    = round_pr(quan, 0.0001);
            this.quantityStr = field_utils.format.float(this.quantity, {digits: [69, 4]});
        }
        this.trigger('change',this);
    },

    });
});
