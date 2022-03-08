odoo.define('membership_pos_info.membership_pos', function (require) {
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
            
            this.member_categories = [];
        
            var partner_model = _.find(this.models, function(model){ return model.model === 'res.partner'; });
            partner_model.fields.push('ref');
            partner_model.fields.push('membership_state');
            partner_model.fields.push('membership_category_ids');
            partner_model.fields.push('membership_category_id');            
            partner_model.fields.push('membership_stop');
            partner_model.fields.push('guarantor_member');
            partner_model.fields.push('free_member');
            partner_model.fields.push('birthdate_date');
            partner_model.fields.push('comment');
            return _super_posmodel.initialize.apply(this, arguments);
        }
    });
    
    models.load_models({
        model: 'membership.membership_category',
        loaded: function(self, categories){
            self.member_categories = categories;
        }
    });
});
