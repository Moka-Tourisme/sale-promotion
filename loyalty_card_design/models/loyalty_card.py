from odoo import api, fields, models
from datetime import timedelta

class LoyaltyCard(models.Model):
    _inherit = 'loyalty.card'

    def create(self, vals_list):
        res = super().create(vals_list)
        for card in res:
            if card.program_id.validity_select == 'date':
                card.expiration_date = card.program_id.validity_date
            else:
                card.expiration_date = fields.Date.today() + timedelta(days=card.program_id.validity_duration)
        return res
