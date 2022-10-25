# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class GiftCardCustom(models.Model):
    _inherit = "gift.card"

    product_id = fields.Many2one('product.template', ondelete='cascade', string="Product", required=True, store=True, readonly=False)

