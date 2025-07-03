from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    expired_profit_account = fields.Many2one('account.account', string='Expired Profit Account',
                                             domain=[('deprecated', '=', False)],
                                             help="Account used to record the expired profit of the gift card.")
    expired_journal = fields.Many2one('account.journal', string='Expired Journal',
                                      help="Journal used to record the expired profit of the gift card.",
                                      default=lambda self: self.env['account.journal'].search([('code', '=', 'OD')],
                                                                                              limit=1))

    def _get_product_accounts(self):
        accounts = super(ProductTemplate, self)._get_product_accounts()
        accounts.update({
            'expired_profit': self.expired_profit_account,
            'journal': self.expired_journal
        })
        return accounts
