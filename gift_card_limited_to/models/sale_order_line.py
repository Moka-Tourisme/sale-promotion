# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from dateutil.relativedelta import relativedelta
from odoo import _, api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _build_gift_card(self):
        gift_card = super()._build_gift_card()
        if self.product_id.limited:
            gift_card['limited'] = self.product_id.limited
            if self.product_id.limited_to == 'product':
                gift_card['limited_to'] = 'product'
                gift_card['limited_to_product_id'] = self.product_id.limited_to_product_id.id
            elif self.product_id.limited_to == 'category':
                gift_card['limited_to'] = 'category'
                gift_card['limited_to_category_id'] = self.product_id.limited_to_category_id.id
            elif self.product_id.limited_to == 'product_list':
                gift_card['limited_to'] = 'product_list'
                gift_card['limited_to_product_list'] = self.product_id.limited_to_product_list.ids
        return gift_card
