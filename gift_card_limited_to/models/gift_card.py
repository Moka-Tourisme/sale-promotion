from odoo import fields, models, api

class GiftCardCustom(models.Model):
    _inherit = "gift.card"

    limited = fields.Boolean(string="Limited usage")

    LIMITED_TO_SELECTION = [
        ('none', 'None'),
        ('product', 'Product'),
        ('category', 'Category'),
        ('product_list', 'Product List'),
    ]

    limited_to = fields.Selection(selection=LIMITED_TO_SELECTION, string="Limitation Type")
    limited_to_product_id = fields.Many2one('product.template', string="Limited Product")
    limited_to_category_id = fields.Many2one('product.category', string="Limited Category")
    limited_to_product_list = fields.Many2many(
        'product.template',
        'gift_card_product_template_limited_product_list_rel',
        'gift_card_id',
        'product_id',
        string="Limited Product List"
    )

    @api.onchange('limited_to')
    def _onchange_limited_to(self):
        self.limited_to_product_id = False
        self.limited_to_category_id = False
        self.limited_to_product_list = False
