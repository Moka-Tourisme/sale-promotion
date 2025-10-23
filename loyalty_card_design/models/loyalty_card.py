from odoo import api, fields, models
from datetime import timedelta

class LoyaltyCard(models.Model):
    _inherit = 'loyalty.card'


    gifter_name = fields.Char(string="Gifter Name", help="Name of the person offering the gift", required=False)
    recipient_name = fields.Char(string="Recipient Name", help="Name of the gift recipient", required=False)
    occasion = fields.Char(string="Occasion", help="Occasion for the gift (Christmas, Birthday, etc.)", required=False)
    valid_for_persons = fields.Integer(string="Valid for Persons", help="Number of persons who can use this card", required=False, default=1)


    def create(self, vals_list):
        res = super().create(vals_list)
        print(vals_list)
        for card in res:
            if card.program_id.validity_select == 'date':
                card.expiration_date = card.program_id.validity_date
            else:
                card.expiration_date = fields.Date.today() + timedelta(days=card.program_id.validity_duration)
        return res
    
