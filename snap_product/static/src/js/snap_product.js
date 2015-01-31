
function snap_product_wd(instance,module){
    var QWeb = instance.web.qweb;
	var _t = instance.web._t;


module.PaymentScreenWidget.include({

    update_payment_summary: function() {

        this._super();


        //SNAP journal code

         var order  = this.pos.get('selectedOrder');
         var selected_paymentline = order.selected_paymentline;

         var currentOrder = this.pos.get('selectedOrder');

        if (selected_paymentline)
        {
            var journal_code = selected_paymentline.cashregister.journal.code;
            var amount = selected_paymentline.amount;
        }

        if (journal_code == 'SNAP') {
            if (amount <= currentOrder.getSnapTotalTaxIncluded()) {


                var paidTotal = currentOrder.getPaidTotal();
                var dueTotal = currentOrder.getSnapTotalTaxIncluded();
                var remaining = dueTotal > paidTotal ? dueTotal - paidTotal : 0;
                var change = paidTotal > dueTotal ? paidTotal - dueTotal : 0;

                this.$('.payment-due-total').html(this.format_currency(dueTotal));
                this.$('.payment-paid-total').html(this.format_currency(paidTotal));
                this.$('.payment-remaining').html(this.format_currency(remaining));
                this.$('.payment-change').html(this.format_currency(change));


            }
            else {

            selected_paymentline.set_amount(0);

            var paidTotal = currentOrder.getPaidTotal();
            var dueTotal = currentOrder.getSnapTotalTaxIncluded();
            var remaining = dueTotal > paidTotal ? dueTotal - paidTotal : 0;
            var change = paidTotal > dueTotal ? paidTotal - dueTotal : 0;

            this.$('.payment-due-total').html(this.format_currency(dueTotal));
            this.$('.payment-paid-total').html(this.format_currency(paidTotal));
            this.$('.payment-remaining').html(this.format_currency(remaining));
            this.$('.payment-change').html(this.format_currency(change));

            if (this.pos_widget.action_bar) {
                this.pos_widget.action_bar.set_button_disabled('validation', true);
                this.pos_widget.action_bar.set_button_disabled('invoice', true);
            }

            }

        }


    }


});




    module.Order = module.Order.extend({


        getSnapTotalTaxExcluded: function() {


          return(this.get('orderLines')).reduce((function(sum, orderLine)
            {

                if(orderLine.get_product().snap_ok) {
                    return sum + orderLine.get_price_without_tax();
                }
                else {
                    return sum;}

            }), 0);


        },


        getSnapTotalTaxIncluded: function() {


          return(this.get('orderLines')).reduce((function(sum, orderLine)
            {

                if(orderLine.get_product().snap_ok) {
                    return sum + orderLine.get_price_with_tax();
                }
                else {
                    return sum;}

            }), 0);


        },

        getSnapDueLeft: function() {
            return this.getSnapTotalTaxIncluded() - this.getPaidTotal();
        },


         addPaymentline: function(cashregister) {
            var self = this;
            var journal = cashregister.journal
            if (journal.debt && ! this.get_client()){
                setTimeout(function(){
                    var ss = self.pos.pos_widget.screen_selector;
                    ss.set_current_screen('clientlist');
                }, 30);
                return;
            }

            var paymentLines = this.get('paymentLines');

            var newPaymentline = new module.Paymentline({},{cashregister:cashregister});



            if(journal.type !== 'cash'){
                var val;
                if (journal.debt)
                    val = -this.getChange() || 0
                else
                    if (journal.code == 'SNAP'){
                        val = this.getSnapDueLeft();
                    }
                    else{
                        val = this.getDueLeft();
                    }


                newPaymentline.set_amount( val );
            }
            paymentLines.add(newPaymentline);
            this.selectPaymentline(newPaymentline);
        }

    });


}
