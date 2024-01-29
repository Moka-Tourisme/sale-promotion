# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from dateutil.relativedelta import relativedelta
from odoo import _, api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _build_gift_card(self):
        gift_card = super()._build_gift_card()
        gift_card['product_template_id'] = self.product_template_id.id
        gift_card['customer_id'] = self.order_partner_id.id
        if self.product_template_id.validity_select == 'duration':
            gift_card['expired_date'] = fields.Date.today() + relativedelta(days=self.product_template_id.validity_duration)
        elif self.product_template_id.validity_select == 'date':
            gift_card['expired_date'] = self.product_template_id.validity_date
        return gift_card

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _send_gift_card_mail(self):
        template = self.env.ref('gift_card_design.mail_template_gift_card_custom', raise_if_not_found=False)
        if template and self.gift_card_count:
            for gift in self.order_line.mapped("generated_gift_card_ids"):
                template.send_mail(gift.id, force_send=True, notif_layout=False)
