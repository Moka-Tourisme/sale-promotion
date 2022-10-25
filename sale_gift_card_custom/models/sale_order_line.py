# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _build_gift_card(self):
        gift_card = super()._build_gift_card()
        gift_card['product_id'] = self.product_template_id.id
        return gift_card