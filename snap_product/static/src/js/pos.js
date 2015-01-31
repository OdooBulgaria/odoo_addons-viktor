function snap_product_at(instance, module){


    var PosModelSuper = module.PosModel
    module.PosModel = module.PosModel.extend({
        load_server_data: function(){
            var self = this;
            var loaded = PosModelSuper.prototype.load_server_data.call(this);

            loaded = loaded.then(function(){
                return self.fetch(
                    'product.product',
                    ['snap_ok'],
                    [['sale_ok','=',true],['available_in_pos','=',true]],
                    {}
                );

            }).then(function(products){
                $.each(products, function(){
                    $.extend(self.db.get_product_by_id(this.id) || {}, this)
                });
                return $.when()
            })
            return loaded;
        }

    })

}

