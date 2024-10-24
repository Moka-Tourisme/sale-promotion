from odoo import fields, models, api

class LoyaltyCardTemplate(models.Model):
    _name = 'loyalty.program'
    _description = 'Loyalty program Card Template'
    _rec_name = 'name'
    _inherit = 'loyalty.program'


    title = fields.Char(translate=True, help='Default title for the gift card')
    title_text_color = fields.Char(readonly=False, default='#000000')

    description = fields.Html('Description', translate=True, help='Description of the gift card')

    balance = fields.Boolean('Balance', help='Display the balance of the gift card')

    condition = fields.Html('Condition', translate=True, help='Condition of the gift card')

    gift_card_header = fields.Binary()
    gift_card_description_image = fields.Binary()

    validity_select = fields.Selection([
        ('duration', 'Duration'),
        ('date', 'Date'),
    ], string='Validity', default='duration', required=True)

    validity_duration = fields.Integer(string='Duration', default=365)

    validity_date = fields.Date(string='Date', default=fields.Date.today)

   

