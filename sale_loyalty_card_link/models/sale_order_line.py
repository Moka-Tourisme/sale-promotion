# Copyright 2026 Moka
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from markupsafe import Markup

from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        for line in lines:
            if (
                line.coupon_id
                and line.coupon_id.program_id.program_type == "gift_card"
                and line.product_id
                and line.order_id.state == "sale"
            ):
                line._update_chatter_with_card_link()
        return lines

    def _update_chatter_with_card_link(self):
        self.ensure_one()
        card = self.coupon_id
        last_msg = self.order_id.message_ids[:1]
        # The sale module posts "Extra line with {product.display_name}" on create.
        # We replace the plain product name with an HTML link to the loyalty card.
        product_name = Markup.escape(self.product_id.display_name)
        if not last_msg or product_name not in last_msg.body:
            return
        card_link = Markup(
            '<a href="/web#model=loyalty.card&amp;id={id}&amp;view_type=form">{name}</a>'
        ).format(id=card.id, name=card.display_name)
        last_msg.sudo().write({"body": last_msg.body.replace(product_name, card_link)})
