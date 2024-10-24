# Copyright 2024 Moka (https://www.moka.cloud).
# @author Horvat Damien <ultrarushgame@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _

class LoyaltyProgram(models.Model):
    _inherit = 'loyalty.program' 

    @api.model
    def _program_type_default_values(self):
        default_values = super(LoyaltyProgram, self)._program_type_default_values()
        
        default_values['gift_card']['rule_ids'] = [(5, 0, 0), (0, 0, {
            'reward_point_amount': 1,
            'reward_point_mode': 'money',
        })]

        default_values['gift_card']['reward_ids'] = [(5, 0, 0), (0, 0, {
            'discount_applicability': 'specific',
        })]
        
        return default_values