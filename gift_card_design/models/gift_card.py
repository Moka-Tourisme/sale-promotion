# Copyright 2022 Moka Tourisme (https://www.mokatourisme.fr).
# @author Romain DUCIEL<romain@mokatourisme.fr>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class GiftCardDesign(models.Model):
    _inherit = "gift.card"

    product_id = fields.Many2one('product.product', string="Product", required=True)

    customer_id = fields.Many2one('res.partner', string="Customer")
