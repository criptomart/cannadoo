odoo.define('pos_cannadoo.pos', function (require) {
  "use strict";
  
  var screens = require('point_of_sale.screens');
  var gui = require('point_of_sale.gui');
  var PopupWidget = require('point_of_sale.popups');

  var core = require('web.core');
  var rpc = require('web.rpc');
  var Dialog = require('web.Dialog');
  var FieldBinaryImage = require('web.basic_fields').FieldBinaryImage;

  var _t = core._t;
  var QWeb = core.qweb;
  
  var img_data;

  // "include" updates original method
  screens.ClientListScreenWidget.include({
    partner_image_url: function(id, field){
        return '/web/image?model=res.partner&id='+id+'&field='+field;
    },
    display_client_details: function(parent, options) {
        this._super(parent, options);
        
        this.uploaded_picture_id = null;
        this.uploaded_picture_id_back = null;

        var self = this,
            WebCamDialog = $(QWeb.render("WebCamDialog")),
            img_data;

        // ::webcamjs:: < https://github.com/jhuckaby/webcamjs >
        // Webcam: Set Custom Parameters
        Webcam.set({
            width: 320,
            height: 240,
            dest_width: 320,
            dest_height: 240,
            image_format: 'jpeg',
            jpeg_quality: 90,
            force_flash: false,
            fps: 45,
            swfURL: '/web_widget_image_webcam/static/src/js/webcam.swf',
        });

        rpc.query({
            model: 'ir.config_parameter',
            method: 'get_webcam_flash_fallback_mode_config',
        }).then(function(default_flash_fallback_mode) {
            if (default_flash_fallback_mode == 1) {
                Webcam.set({
                    /*
                        :: Important Note about Chrome 47+ :: < https://github.com/jhuckaby/webcamjs#important-note-for-chrome-47 >
                        Setting "force_flash" to "true" will always run in Adobe Flash fallback mode on Chrome, but it is not desirable.
                    */
                    force_flash: true,
                });
            }
        });        
        
        this.$('.o_form_binary_file_web_cam').click(function(el){
            self.gui.show_popup('webcam_scan',{
                'title': _t('Toma de fotos'),
                value: el,      
            });
        });
        
        this.$('#picUpload').on('change',function(event){
            if (event.target.files.length) {
                self.load_image_file(event.target.files[0],function(res){
                    if (res) {
                        $('.client-picture-cannadoo img, .client-picture .fa').remove();
                        $('.client-picture-cannadoo').append("<img src='"+res+"'>");
                        $('.detail.picture-cannadoo').remove();
                        self.uploaded_picture = res;
                    }
                });
            }
        });
        
        this.$('#picUploadId').on('change',function(event){
            if (event.target.files.length) {
                self.load_image_file(event.target.files[0],function(res){
                    if (res) {
                        $('.client-picture-cannadoo-id').children().remove();
                        $('.client-picture-cannadoo-id').append("<img src='"+res+"' height='250px' >");
                        self.uploaded_picture_id = res;
                    }
                });
            }
        });
        
        this.$('#picUploadIdBack').on('change',function(event){
            if (event.target.files.length) {
                self.load_image_file(event.target.files[0],function(res){
                    if (res) {
                        $('.client-picture-cannadoo-id-back').children().remove();
                        $('.client-picture-cannadoo-id-back').append("<img src='"+res+"' height='250px' >");
                        self.uploaded_picture_id_back = res;
                    }
                });
            }
        });
        
        this.$('#filter_guarantor').on('input',function(event){
            var filter = $('#filter_guarantor').val().toUpperCase();
            if(filter){
                var partners = self.pos.db.get_partners_sorted();
                // Filter partners and set select options
                for (var i = 0; i < partners.length; i++){
                    var partner = partners[i];
    //                console.log("partner: " + partner.ref + " - " + partner.name);
                    if (filter == partner.ref){
                        $('.client-guarantor').val(partner.id);
                        break;
                    }
                    else if(filter == partner.barcode){
                        $('.client-guarantor').val(partner.id);
                        break;
                    }
                    else if(partner.name.toLowerCase().includes(filter.toLowerCase())){
                        $('.client-guarantor').val(partner.id);
                        break;
                    }
                }
            }
        });                
    },
    
    save_client_details: function(partner) {
        var self = this;
        
        var fields = {};
        this.$('.client-details-contents .detail').each(function(idx,el){
            fields[el.name] = el.value || false;
        });

        fields.free_member = $("#free_member").is(":checked")
        
        // Check required fields
        if (!fields.name) {
            this.gui.show_popup('error',_t('A Customer Name Is Required'));
            return;
        }
        
        if (!fields.vat) {
            this.gui.show_popup('error',_t('El campo NIF es requerido'));
            return;
        } else{
            fields.vat = fields.vat.toUpperCase();
            if(fields.vat.substring(0,2) != "EU"){
                if(!this.validate_vat(fields.vat)){
                    this.gui.show_popup('error',_t('El campo NIF no es válido en España. Para saltar la validación en NIF extranjeros añade "EU" delante del número'));
                    return;
                }
            }
        }

        if (!fields.birthdate_date) {
            this.gui.show_popup('error',_t('El campo fecha de nacimiento es requerido'));
            return;
        }

        if (!fields.guarantor_member) {
            this.gui.show_popup('error',_t('El campo Aval es requerido'));
            return;
        }
        
        // Get uploaded pictures
        if (self.uploaded_picture){
            fields.image = self.uploaded_picture;
        }
        if (self.uploaded_picture_id){
            fields.image_id = self.uploaded_picture_id;
        }
        if (self.uploaded_picture_id_back){
            fields.image_id_back = self.uploaded_picture_id_back;
        }        
        
        if (fields.image_id) {
            fields.image_id = fields.image_id.split(",")[1];
        }

        if (fields.image_id_back) {
            fields.image_id_back = fields.image_id_back.split(",")[1];
        }
        
        fields.id           = partner.id || false;
        fields.country_id   = fields.country_id || false;

        if (fields.property_product_pricelist) {
            fields.property_product_pricelist = parseInt(fields.property_product_pricelist, 10);
        } else {
            fields.property_product_pricelist = false;
        }
        var contents = this.$(".client-details-contents");
        contents.off("click", ".button.save");


        rpc.query({
                model: 'res.partner',
                method: 'create_from_ui',
                args: [fields],
            })
            .then(function(partner_id){
//                self.partner_cache.clear_node(partner_id);
                self.saved_client_details(partner_id);
            },function(err,ev){
                ev.preventDefault();
                var error_body = _t('Your Internet connection is probably down.');
                if (err.data) {
                    var except = err.data;
                    error_body = except.arguments && except.arguments[0] || except.message || error_body;
                }
                self.gui.show_popup('error',{
                    'title': _t('Error: Could not Save Changes'),
                    'body': error_body,
                });
                contents.on('click','.button.save',function(){ self.save_client_details(partner); });
            });
    },
    validate_vat: function(vat){
        // Comprueba si es un DNI correcto (entre 5 y 8 letras seguidas de la letra que corresponda).

        // Acepta NIEs (Extranjeros con X, Y o Z al principio)
        var numero, caracter, letra;
        var expresion_regular_dni = /^[XYZ]?\d{5,8}[A-Z]$/;

        vat = vat.toUpperCase();

        if(expresion_regular_dni.test(vat) === true){
            numero = vat.substr(0,vat.length-1);
            numero = numero.replace('X', 0);
            numero = numero.replace('Y', 1);
            numero = numero.replace('Z', 2);
            caracter = vat.substr(vat.length-1, 1);
            numero = numero % 23;
            letra = 'TRWAGMYFPDXBNJZSQVHLCKET';
            letra = letra.substring(numero, numero+1);
            if (letra != caracter) {
                //alert('Dni erroneo, la letra del NIF no se corresponde');
                return false;
            }else{
                //alert('Dni correcto');
                return true;
            }
        }else{
            //alert('Dni erroneo, formato no válido');
            return false;
        }
    }
  });
  
  var WebcamPopupWidget = PopupWidget.extend({
        template: "WebcamPopupWidget",
        
        show: function(options) {
            this.gUM = false;
            this._super(options);
            this.generate_webcam(options.value.target);
        },
        click_cancel: function() {
            this.stop_camera();
            this._super(arguments);
        },
        stop_camera: function(camera) {
            this.cam_is_on = false;
            if (this.stream) {
                this.stream.getTracks()[0].stop();
            }
        },
        add_button: function(content) {
            var button = document.createElement("div");
            button.className = "button qr-content";
            button.innerHTML = content.name;
            button.setAttribute("camera-id", content.id);
            button = $(".transparent_sidebar > .body").append(button);
            return button;
        },
        add_button_click: function(e) {
            var button = document.createElement("div");
            var active_id = e.target.getAttribute("camera-id");
            this.start_webcam({deviceId: {exact: active_id}});
            this.pos.db.save("active_camera_id", active_id);
            return button;
        },
        get_camera_by_id: function(id) {
            return _.find(this.video_devices, function(cam) {
                return cam.deviceId === id;
            });
        },
        generate_webcam: function(target) {
            var options = false;
            var self = this;
            
            Webcam.attach('#live_webcam_canna');

            // At time of Init "Save & Close" button is disabled
            $('.save_close_btn').attr('disabled', 'disabled');

            // Placeholder Image in the div "webcam_result_canna"
            this.$("#webcam_result_canna").html('<img src="/web_widget_image_webcam/static/src/img/webcam_placeholder.png"/>');
                
            this.$(".take_snap_btn").click(function(){
                Webcam.snap( function(data) {
                    img_data = data;
                    // Display Snap besides Live WebCam Preview
                    $("#webcam_result_canna").html('<img src="'+img_data+'"/>');
                });
                if (Webcam.live) {
                    // Remove "disabled" attr from "Save & Close" button
                    $('.save_close_btn').removeAttr('disabled');
                }
            });

            this.$('.save_btn').click(function(){
                while($(target).prop("tagName") != "DIV"){
                    target = $(target).parent();
                }
                $(target).children().remove();
                $(target).append('<img src="'+img_data+'" height="250px" />');
                $(target).append('<input class="detail oe_hidden" name="' + $(target).attr("id") + '" value="' + img_data + '"/>');
                self.click_cancel();                
            });
            
            this.$('.close_btn').click(function(){
                self.click_cancel();
            });        
        },
    });

    gui.define_popup({name: "webcam_scan", widget: WebcamPopupWidget});  
})

