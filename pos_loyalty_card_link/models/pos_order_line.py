# Copyright 2026 Moka
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        for line in lines:
            if (
                line.coupon_id
                and line.coupon_id.program_id.program_type == "gift_card"
                and line.coupon_id.code
            ):
                code = line.coupon_id.code
                current_name = line.full_product_name or ""
                if code not in current_name:
                    line.full_product_name = f"{current_name} ({code})" if current_name else code
        return lines
