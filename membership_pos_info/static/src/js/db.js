odoo.define('membership_pos_info', function (require) {

    "use strict";
    var db = require("point_of_sale.DB");
    db.include({

    _partner_search_string: function(partner){
        var str =  partner.name;
        if(partner.barcode){
            str += '|' + partner.barcode;
        }
        if(partner.vat){
            str += '|' + partner.vat;
        }
        if(partner.ref){
            str += '|' + partner.ref;
        }
        str = '' + partner.id + ':' + str.replace(':','') + '\n';
        return str;
        },
    });

    return db;

});
