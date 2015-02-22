



function screen_hd(instance, module){

module.PosDB  =  module.PosDB.extend({


        get_product_by_category: function(category_id) {

            var list = this._super(category_id);


            if (category_id == 0){

                list = 0;
            }


        return list;

  }


    })


















}

