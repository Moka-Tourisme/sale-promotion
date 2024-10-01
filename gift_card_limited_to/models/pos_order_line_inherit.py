# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from dateutil.relativedelta import relativedelta
from odoo import fields, models


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    def _build_gift_card(self):
        gift_card = super()._build_gift_card()
        limited_to_product_id = False
        if self.product_id:
            if self.product_id.product_tmpl_id.limited:
                if self.product_id.product_tmpl_id.limited_to == 'product':
                    limited_to_product_id = self.product_id.product_tmpl_id.limited_to_product_id.id
                elif self.product_id.product_tmpl_id.limited_to == 'category':
                    limited_to_product_id = self.product_id.product_tmpl_id.limited_to_category_id.id
                elif self.product_id.product_tmpl_id.limited_to == 'product_list':
                    limited_to_product_id = self.product.product_tmpl_id.limited_to_product_list.ids
                elif self.product_id.product_tmpl_id.limited_to == 'none':
                    limited_to_product_id = False
                gift_card['limited_to_product_id'] = limited_to_product_id
            else :
                gift_card['limited_to_product_id'] = False

        return gift_card