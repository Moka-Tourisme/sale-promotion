from odoo import fields, models, api


class LoyaltyCardTemplate(models.Model):
    _name = 'loyalty.program'
    _description = 'Loyalty program Card Template'
    _rec_name = 'name'
    _inherit = 'loyalty.program'

    logo = fields.Binary('Logo', help='Logo of the gift card')
    logo_width = fields.Integer('Logo Width', default=90, help='Width of the logo in px')
    logo_height = fields.Integer('Logo Height', default=140, help='Height of the logo in px')
    logo_position = fields.Integer('Logo Position', default=0, help="0 to 100. Corresponds to the top property in css")

    title = fields.Char(translate=True,
                                  help='Title of the gift card, if not set, the name of the product will be used')
    title_text_color = fields.Char(readonly=False, default='#856846')

    description = fields.Html('Description', translate=True, help='Description of the gift card')

    condition = fields.Html('Condition', translate=True, help='Condition of the gift card')

    balance = fields.Boolean(default=True, string='Display Balance on Gift Card',
                                       help='Display the balance on the gift card')
    balance_text_color = fields.Char(readonly=False, default='#ffffff')
    balance_background_color = fields.Char(readonly=False, default='#e84d0e')

    primary_background_color = fields.Char(readonly=False, default='#f5efd6')
    secondary_background_color = fields.Char(readonly=False, default='#F9F6EA')
    text_color = fields.Char(readonly=False, default='#445161')

    gift_card_header = fields.Binary()
    gift_card_description_image = fields.Binary()

    validity_select = fields.Selection([
        ('duration', 'Duration'),
        ('date', 'Date'),
    ], string='Validity', default='duration', required=True)

    validity_duration = fields.Integer(string='Duration', default=365)

    validity_date = fields.Date(string='Date', default=fields.Date.today)

    show_gifter_info = fields.Boolean(string="Show Gifter Information", default=True, 
                                    help="Display who is offering the gift card")
    show_recipient_info = fields.Boolean(string="Show Recipient Information", default=True,
                                        help="Display who receives the gift card")
    show_occasion = fields.Boolean(string="Show Occasion", default=True,
                                help="Display the occasion for the gift")
    show_valid_for_persons = fields.Boolean(string="Show Valid for X Persons", default=False,
                                            help="Display how many persons can use the card")
    
    show_validity_info = fields.Boolean(string="Show Validity date", default=False,
                                            help="Display a validity date")

    default_valid_for_persons = fields.Integer(string="Default Valid for Persons", default=1)

    physic_card = fields.Boolean(string="Physical gift card", default=False)
    physical_gift_card_product_id = fields.Many2one('product.product', 
                                                    string="Physical Gift Card Product",
                                                    help="Product used for physical gift cards")
