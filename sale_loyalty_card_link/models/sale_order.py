# Copyright 2026 Moka
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _get_reward_line_values(self, reward, coupon, **kwargs):
        values_list = super()._get_reward_line_values(reward, coupon, **kwargs)
        if reward.program_id.program_type == "gift_card" and coupon.code:
            for vals in values_list:
                vals["name"] = f"{vals['name']} ({coupon.code})"
        return values_list
