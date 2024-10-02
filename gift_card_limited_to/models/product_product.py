from odoo import fields, models, api

class ProductTemplateCustom(models.Model):
    _inherit = "product.template"

    limited = fields.Boolean(string="Limited usage")

    LIMITED_TO_SELECTION = [
        ('none', 'None'),
        ('product', 'Product'),
        ('category', 'Category'),
        ('product_list', 'Product List'),
    ]

    limited_to = fields.Selection(selection=LIMITED_TO_SELECTION, string="Limited to", default='none')
    limited_to_product_id = fields.Many2one('product.template', string="Product", help="The specific product to which this product is limited.")
    limited_to_category_id = fields.Many2one('product.category', string="Category", help="The category of products to which this product is limited.")
    limited_to_product_list = fields.Many2many(
    'product.template',
    'product_template_limited_product_list_rel',
    'product_id',
    'related_product_id',
    string="Limited Product List"
)

    @api.onchange('limited_to')
    def _onchange_limited_to(self):
        self.limited_to_product_id = False
        self.limited_to_category_id = False
        self.limited_to_product_list = False