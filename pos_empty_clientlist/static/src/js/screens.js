// Copyright 2021 Criptomart <https://criptomart.net>
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

odoo.define('pos_empty_clientlist.screens', function (require) {
    "use strict";

    var screens = require('point_of_sale.screens');

    screens.ClientListScreenWidget.include({
        show: function() {
            this._super();
            this.$('.client-list-contents').hide();
        },
        perform_search: function(query, associate_result){
            this.$('.client-list-contents').show();
            this._super(query, associate_result);
        },        
    });
    
    return screens;
});
