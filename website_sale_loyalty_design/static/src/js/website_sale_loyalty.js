odoo.define('website_sale_loyalty_design.gift_card_form', function (require) {
    'use strict';

    let publicWidget = require('web.public.widget');
    let ajax = require('web.ajax');

    publicWidget.registry.GiftCardCustomForm = publicWidget.Widget.extend({
        selector: '.oe_website_sale',
        events: {
            'click #save_gift_card_info': '_onSaveGiftCardInfo',
        },

        start: function () {
            this._super.apply(this, arguments);
            return this._super.apply(this, arguments);
        },

        _onSaveGiftCardInfo: function (ev) {
            ev.preventDefault();
            console.log("Click sur le bouton de sauvegarde");
            $('.oe_gift_card_custom_info .alert').remove();
            let formData = {};
            let form = this.$('#gift_card_form')[0];
            let formElements = form.elements;
            console.log("Formulaire :", formElements);
            
            for (let i = 0; i < formElements.length; i++) {
                console.log("boucle for");
                let element = formElements[i];
                console.log(element);
                if (element.name && element.name.startsWith('gift_card')) {
                    console.log("Analyse de :", element.name);
                    formData[element.name] = element.value;
                    console.log("La valeur est :", formData[element.name]);
                }
            }
            
            console.log("Requête RPC");

            this._rpc({
                route: '/shop/cart/update_gift_info',
                params: formData,
            }).then(function (result) {
                if (result.success) {
                    let alertHtml = '<div class="alert alert-success alert-dismissible fade show" role="alert">' +
                        '<i class="fa fa-check me-1"></i>' + result.message +
                        '<button type="button" class="btn-close" data-bs-dismiss="alert"></button>' +
                        '</div>';
                    $('.oe_gift_card_custom_info .card-body').prepend(alertHtml);
                } else {
                    console.error('Error updating gift card info:', result.error);
                }
            });
        },

    });

    return publicWidget.registry.GiftCardCustomForm;
});
