/**
    Copyright (C) 2021: Criptomart (https://criptomart.net)
    @author: Criptomart (https://criptomart.net)
    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
*/

odoo.define('membership_cannadoo.models', function (require) {
    "use strict";

    var field_utils = require('web.field_utils');
    var utils = require('web.utils');
    var models = require('point_of_sale.models');
    var round_di = utils.round_decimals;
    var round_pr = utils.round_precision;

   var _super_posmodel = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        initialize: function (session, attributes) {
            var partner_model = _.find(this.models, function(model){ return model.model === 'res.partner'; });
            partner_model.fields.push('membership_category_id');
            partner_model.fields.push('property_product_pricelist');
            return _super_posmodel.initialize.apply(this, arguments);
        }
    });

    var order_super = models.Order.prototype;

    models.Order = models.Order.extend({

      initialize: function(attr, options){
           order_super.initialize.apply(this, arguments);
      },
/*
      set_client: function(client){
          console.log("client");
          console.log(client);
          //order_super.initialize.apply(this, arguments);
          this.assert_editable();
          this.set('client',client);
          if (client.membership_category_id && client.membership_pricelist) {
              console.log("cat " + client.membership_category_id + " -- pricelist " + client.membership_pricelist);
              this.set_pricelist(client.membership_pricelist);
          }
      },
*/

      set_pricelist: function (pricelist) {
          var self = this;
          var old_pricelist = this.pricelist;  
          this.pricelist = pricelist;
          //var lines_to_recompute = _.filter(this.get_orderlines(), function (line) {
          //    return ! line.price_manually_set;
          //});
          var lines_to_recompute = this.get_orderlines();
          _.each(lines_to_recompute, function (line) {
              if (line.product.uom_id[1] === "g") {
                var old_price = line.product.get_price(old_pricelist, 1);
                line.set_unit_price(old_price * line.get_quantity());
              } else {
                line.set_unit_price(line.product.get_price(self.pricelist, 1));
              }
              //self.fix_tax_included_price(line);
          });
          this.trigger('change');
    },


    });
});
