# Copyright 2024 Moka (https://www.moka.cloud/).
# @author Damien Horvat <damien@moka.cloud>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from datetime import timedelta


class LoyaltyCard(models.Model):
    _inherit = "loyalty.card"


    def create(self, vals_list):
        res = super().create(vals_list)
        if res.program_id.validity_type == 'fixed':
            res.expiration_date = res.program_id.date_to
        else:
            res.expiration_date = fields.Date.today() + timedelta(days=res.program_id.validity_duration)
        return res
