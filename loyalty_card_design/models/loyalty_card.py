from odoo import api, fields, models
from datetime import timedelta

class LoyaltyCard(models.Model):
    _inherit = 'loyalty.card'

    def create(self, vals_list):
        res = super().create(vals_list)
        if res.program_id.validity_select == 'date':
            res.expiration_date = res.program_id.validity_date
        else:
            res.expiration_date = fields.Date.today() + timedelta(days=res.program_id.validity_duration)
        return res
