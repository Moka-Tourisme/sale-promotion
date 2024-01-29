# Copyright 2022 Moka Tourisme (https://www.mokatourisme.fr).
# @author Romain DUCIEL<romain@mokatourisme.fr>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError

class ProductTemplate(models.Model):
    _inherit = "product.template"
    company_id = fields.Many2one(
        'res.company', default=lambda self: self.env.company, required=True)

    gift_card_title = fields.Char(translate=True, help='Title of the gift card, if not set, the name of the product will be used')
    title_text_color = fields.Char(readonly=False, default='#000000')
    title_background_color = fields.Char(readonly=False, default='#ffffff')

    gift_card_description = fields.Html('Description', translate=True, help='Description of the gift card')
    description_text_color = fields.Char(readonly=False, default='#000000')
    description_background_color = fields.Char(readonly=False, default='#ffffff', store=True)

    gift_card_condition = fields.Html('Condition', translate=True, help='Condition of the gift card')
    condition_text_color = fields.Char(readonly=False, default='#000000')
    condition_background_color = fields.Char(readonly=False, default='#ffffff')

    gift_card_balance = fields.Boolean(default=True, string='Display Balance on Gift Card', help='Display the balance on the gift card')
    balance_text_color = fields.Char(readonly=False, default='#000000')
    balance_background_color = fields.Char(readonly=False, default='#ffffff')

    code_background_color = fields.Char(readonly=False, default='#ffffff')

    gift_card_header = fields.Binary()

    validity_select = fields.Selection([
        ('duration', 'Duration'),
        ('date', 'Date'),
    ], string='Validity', default='duration', required=True)

    validity_duration = fields.Integer(string='Duration', default=365)

    validity_date = fields.Date(string='Date', default=fields.Date.today)

    @api.ondelete(at_uninstall=False)
    def _unlink_gift_card_product(self):
        if self.env.ref('gift_card.pay_with_gift_card_product').product_tmpl_id in self:
            raise UserError(_('Deleting the Gift Card Pay product is not allowed.'))
