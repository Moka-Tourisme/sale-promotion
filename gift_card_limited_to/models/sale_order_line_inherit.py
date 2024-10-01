# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from dateutil.relativedelta import relativedelta
from odoo import _, api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _build_gift_card(self):
        gift_card = super()._build_gift_card()
        limited_to_product_id = False
        if self.product_id.limited:
            if self.product_id.limited_to == 'product':
                limited_to_product_id = self.product_id.limited_to_product_id.id
            elif self.product_id.limited_to == 'category':
                limited_to_product_id = self.product_id.limited_to_category_id.id
            elif self.product_id.product_tmpl_id.limited_to == 'product_list':
                limited_to_product_id = self.product.product_tmpl_id.limited_to_product_list.ids
        gift_card['limited_to_product_id'] = limited_to_product_id
        return gift_card
