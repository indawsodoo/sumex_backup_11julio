odoo.define('indaws_affinity_e_commerce_mvp_payment.update_qty', function(require) {
    'use strict';

    var ajax = require('web.ajax');
    var rpc = require('web.rpc');
    var core = require('web.core');
    var QWeb = core.qweb;

    var WebsiteSale = require("website_sale.website_sale");
    var webAnimations = require('website.content.snippets.animation');
    var _t = core._t;

    webAnimations.registry.WebsiteSale.include({

        init: function(parent, options) {
            this.events["click .js_add_cart_json_indaws_remove"] = "_removeQtyCart";
            this.events["click .js_add_cart_json_indaws"] = "_addQtyCart";
            this.events["change .quantity"] = "_changeInputQty";
            this._super(parent, options);
        },

        _removeQtyCart: function (ev) {
            var $link = $(ev.currentTarget);
            var input = $link.closest('.input-group-prepend').find("span#sh_descrement_qty_test").text();
            if (parseInt($link.closest('.css_quantity').find("input.quantity").val()) - parseInt(input) > 0){
                var total = parseInt($link.closest('.css_quantity').find("input.quantity").val()) - parseInt(input)
                $link.closest('.css_quantity').find("input.quantity").val(total)
           }
        },
        _addQtyCart: function (ev) {
            var $link = $(ev.currentTarget);
            var $input = $link.closest('.input-group-append').find("span#sh_increment_qty_test").text();
            var total = parseInt($link.closest('.css_quantity').find("input.quantity").val()) + parseInt($input)
            $link.closest('.css_quantity').find("input.quantity").val(total)
        },
        _changeInputQty: function (ev) {
            var $link = $(ev.currentTarget);
            var default_value = $link.closest('.css_quantity').find("input.quantity").data("setqty");
            var data = parseInt($link.closest('.css_quantity').find("input.quantity").val());
            var divided_value = Math.ceil(data / parseInt(default_value));
            var set_data = divided_value * parseInt(default_value);
            $link.closest('.css_quantity').find("input.quantity").val(set_data)
        },

        _onClickAdd: function (ev) {
            var $aSubmit = $(ev.currentTarget);
            var frm = $aSubmit.closest('form');
            var product_product = frm.find('input[name="product_id"]').val();
            var quantity = frm.find('.quantity').val();
            if(!quantity) {
               quantity = 1;
            }
            ajax.jsonRpc(
                '/shop/cart/update_json',
                'call',
                {
                    'product_id': parseInt(product_product),
                    'add_qty': parseInt(quantity),
                    'set_qty': parseInt(quantity)
                }).then(function(data) {
                    if (parseInt(($('.my_cart_quantity')[0].innerHTML)) == 0){
                        $('.my_cart_quantity')[0].innerHTML = parseInt(data['cart_quantity'])
                    }
                    else{
                        $('.my_cart_quantity')[0].innerHTML = parseInt(($('.my_cart_quantity')[0].innerHTML)) + data['quantity'];
                    }
            });
             self._rpc({
                        route: '/ajax_cart_sucess_data_1',
                        params: {
                            product_id: product_product,
                            product_product: product_product,
                        },
                    }).then(function(data){
                    if($("#wrap").hasClass('js_sale')) {
                            $("#ajax_cart_model_shop .modal-body").html(data);
                            $("#ajax_cart_model_shop").modal({keyboard: true});
                        } else {
                            $("#ajax_cart_model .modal-body").html(data);
                            $("#ajax_cart_model").modal({keyboard: true});
                        }
                        $('#ajax_cart_model, #ajax_cart_model_shop').removeClass('ajax-cart-item');
                        $('#ajax_cart_model, #ajax_cart_model_shop').addClass('ajax-sucess');
                    });
                  return false;
        },
    });


});