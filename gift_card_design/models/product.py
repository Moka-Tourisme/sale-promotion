# Copyright 2022 Moka Tourisme (https://www.mokatourisme.fr).
# @author Romain DUCIEL<romain@mokatourisme.fr>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError

class ProductTemplate(models.Model):
    _inherit = "product.template"

    gift_card_title = fields.Char(translate=True)

    gift_card_description = fields.Html('Description', translate=True)

    gift_card_condition = fields.Html('Condition', translate=True)

    gift_card_balance = fields.Boolean(default=True)

    gift_card_header = fields.Binary()

    @api.ondelete(at_uninstall=False)
    def _unlink_gift_card_product(self):
        if self.env.ref('gift_card.pay_with_gift_card_product').product_tmpl_id in self:
            raise UserError(_('Deleting the Gift Card Pay product is not allowed.'))
