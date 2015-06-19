    
function pos_access_ext_screens (instance, module){

    // Extend PopupWidget to show our own message
    module.AccessPopupWidget = module.PopUpWidget.extend({
        template:'AccessPopupWidget',

        order_ex: function(pass, value, type) {
            var self = this;
            var secret = this.pos.config.secret_access;

            if (pass == secret && pass.length > 0 && secret.length > 0 )
                {
                    var order = this.pos.get('selectedOrder');

                    if ( type == 'discount') {
                        order.getSelectedLine().set_discount(value);
                    }
                    else if( type == 'price') {
                        order.getSelectedLine().set_unit_price(value);
                    }


                    return true;
                }
            return false;

        },


        show: function(){
            this._super();
            var self = this;
            
            this.$el.find('.button_ok').off('click').click(function(){

                var password_ae = $("input[name=password]").val();
                var value_ae = $("input[name=value]").val();
                var type_ae =  $("label[name=mode]").text();
                var result = self.order_ex(password_ae,value_ae, type_ae);

                if (result)
                {
                    self.pos_widget.screen_selector.close_popup();
                }
                else
                {
                    $("input[name=password]").addClass("error");
                }
            });

            this.$el.find('.button_close').off('click').click(function(){

                    self.pos_widget.screen_selector.close_popup();
            });


        }
    });


  }