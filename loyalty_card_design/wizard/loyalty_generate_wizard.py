from odoo import api, fields, models
from dateutil.relativedelta import relativedelta

class LoyaltyGenerateWizard(models.TransientModel):
    _inherit = 'loyalty.generate.wizard'

    valid_until = fields.Date(compute='_compute_valid_until', store=True)

    @api.depends('program_id')
    def _compute_valid_until(self):
        for wizard in self:
            if wizard.program_id:
                program = wizard.program_id
                if program.validity_select == 'duration':
                    wizard.valid_until = fields.Date.today() + relativedelta(days=program.validity_duration)
                elif program.validity_select == 'date':
                    wizard.valid_until = program.validity_date
                else:
                    wizard.valid_until = False
