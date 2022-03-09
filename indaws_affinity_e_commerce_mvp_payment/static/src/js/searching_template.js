odoo.define('indaws_affinity_e_commerce_mvp_payment.productsSearchBar', function (require) {
    'use strict';

    const concurrency = require('web.concurrency');
    const publicWidget = require('web.public.widget');

    publicWidget.registry.productsSearchBar.include({
        xmlDependencies: ['/indaws_affinity_e_commerce_mvp_payment/static/src/xml/website_sale_utils.xml'],
        /**
         * @private
         */
        init: function () {
            this._super.apply(this, arguments);
            this.session = this.getSession()
        },

    });
});