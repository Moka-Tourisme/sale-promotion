# Copyright 2024 Moka (https://www.moka.cloud).
# @author Horvat Damien <ultrarushgame@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from collections import defaultdict

from odoo import _, api, fields, models 
from odoo.exceptions import UserError, ValidationError

from uuid import uuid4

class LoyaltyCard(models.Model): 
    _inherit = 'loyalty.card'
    
    program_type = fields.Selection(related='program_id.program_type', store=True)

    program_reward_ids = fields.One2many('loyalty.reward', compute='_compute_program_reward_ids', string='Program Rewards')


    @api.depends('program_id')
    def _compute_program_reward_ids(self):
        for card in self:
            card.program_reward_ids = card.program_id.reward_ids if card.program_id else []
    
    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for card in res:
            reward = card.program_id.reward_ids
        res._send_creation_communication()
        return res