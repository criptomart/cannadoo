// Copyright 2021 Criptomart <https://criptomart.net>
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

odoo.define('membership_monthly_consumption.membership_pos', function (require) {
    "use strict";

    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');
    var core = require('web.core');
    var gui = require('point_of_sale.gui');
    var _t = core._t;

/* ********************************************************
Overload models.PosModel
******************************************************** */
    var _super_posmodel = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        initialize: function (session, attributes) {
            var partner_model = _.find(this.models, function(model){ return model.model === 'res.partner'; });
            partner_model.fields.push('monthly_consumption_current');
            partner_model.fields.push('monthly_consumption_limit');
            return _super_posmodel.initialize.apply(this, arguments);
        }
    });
    
    // The action pad contains the payment button and the 
    // customer selection button
    screens.ActionpadWidget.include({
        renderElement: function() {
            var self = this;
            this._super();
            this.$('.pay').click(function(){
                var order = self.pos.get_order();
                var client = order.get_client();
                var current_consum = client.monthly_consumption_current;
                var orderlines = order.get_orderlines();
                var grams_in_order = false;
                
                for(var i = 0; i < orderlines.length; i++){
                    var line = orderlines[i];
                    if(line.product.uom_id[1] == 'g'){
                        grams_in_order = true;
                        current_consum += line.get_quantity();
                    }
                }
                if((current_consum > client.monthly_consumption_limit) && (grams_in_order)){
                    self.gui.show_popup('confirm',{
                        'title': _t('Consumo mensual excedido'),
                        'body':  _t('Este socio excede su consumo máximo mensual con esta dispensa. ¿Quieres continuar?'),
                        cancel: function(){
                            this.gui.show_screen('products');
                        }
                    });
                }
            });
            this.$('.set-customer').click(function(){
                self.gui.show_screen('clientlist');
            });
        }
    });
});
