# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
import base64


class PosOrder(models.Model):
    _inherit = "pos.order"

    @api.model
    def create_from_ui(self, orders, draft=False):
        order_ids = super(PosOrder,self).create_from_ui(orders, draft)
        for order in self.sudo().browse([o["id"] for o in order_ids]):
            gift_card_config = order.config_id.gift_card_settings
            for line in order.lines:
                # Change condition and check if the object is a gift card to create gift card and not only when the object is the configured gift card
                if line.product_id.detailed_type == "gift":
                # End of condition
                    if not line.gift_card_id:
                        if gift_card_config == "create_set":
                            new_card = line._create_gift_cards()
                            new_card.partner_id = order.partner_id or False
                            line.generated_gift_card_ids = new_card
                        else:
                            gift_card = self.env["gift.card"].search(
                                [("id", "=", line.generated_gift_card_ids.id)]
                            )
                            gift_card.buy_pos_order_line_id = line.id
                            gift_card.expired_date = fields.Date.add(
                                fields.Date.today(), years=1
                            )
                            gift_card.partner_id = order.partner_id or False

                            if gift_card_config == "scan_set":
                                gift_card.initial_amount = line.price_unit
        return order_ids

    def _add_mail_attachment(self, name, ticket):
        attachment = super()._add_mail_attachment(name, ticket)
        self.ensure_one()
        if self.config_id.use_gift_card and len(self.get_new_card_ids()) > 0:
            report = self.env.ref('gift_card_design.gift_card_custom_report')._render_qweb_pdf(self.get_new_card_ids())
            filename = name + '.pdf'
            gift_card = self.env['ir.attachment'].create({
                'name': filename,
                'type': 'binary',
                'datas': base64.b64encode(report[0]),
                'store_fname': filename,
                'res_model': 'pos.order',
                'res_id': self.id,
                'mimetype': 'application/x-pdf'
            })
            attachment += [(4, gift_card.id)]

        return attachment