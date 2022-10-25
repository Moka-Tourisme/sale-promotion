# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    detailed_type = fields.Selection(selection_add=[
        ('gift', 'Gift Card'),
    ], ondelete={'gift': 'set service'})

    type = fields.Selection(selection_add=[
        ('gift', 'Gift Card')
    ], ondelete={'product': 'set service'})

    title = fields.Char(translate=True)

    description_card = fields.Html('Description', translate=True)

    condition_card = fields.Html('Condition', translate=True)

    show_balance = fields.Boolean(default=True)

    custom_header = fields.Binary()

    def _detailed_type_mapping(self):
        type_mapping = super()._detailed_type_mapping()
        type_mapping['gift'] = 'gift'
        return type_mapping

    @api.ondelete(at_uninstall=False)
    def _unlink_gift_card_product(self):
        if self.env.ref('gift_card.pay_with_gift_card_product').product_tmpl_id in self:
            raise UserError(_('Deleting the Gift Card Pay product is not allowed.'))
