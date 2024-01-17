from odoo import api, fields, models


class Giftcard(models.Model):
    _inherit = 'gift.card'

    expired_profit_account = fields.Many2one('account.account', string='Expired Profit Account',
                                             help="Account used to record the expired profit of the gift card.")
    balance = fields.Monetary(compute="_compute_balance", store=True)  # in company currency

    @api.depends('state')
    def _compute_balance(self):
        super()._compute_balance()
        for record in self:
            account_move_line = self.env['account.move.line'].search([
                ('name', '=', record.code),
                ('debit', '=', record.balance)
            ])
            if account_move_line and record.state == 'expired':
                record.balance = 0

    @api.autovacuum
    def _gc_mark_expired_gift_card(self):
        gift_card_to_expire = self.env['gift.card'].search([
            '&', ('state', '=', 'valid'), ('expired_date', '=', fields.Date.today())
        ])
        if gift_card_to_expire:
            self._create_update_account_move_line(gift_card_to_expire)


    def _cron_gift_card_expired(self):
        gift_card_expired_with_balance = self.env['gift.card'].search([
            ('state', '=', 'expired'), ('balance', '>', 0)
        ])
        self._gc_mark_expired_gift_card()
        # self._create_update_account_move_line(gift_card_expired_with_balance)

    def _create_update_account_move_line(self, gift_cards):
        for gift_card in gift_cards:
            if gift_card.buy_pos_order_line_id:
                accounts = gift_card.buy_pos_order_line_id.product_id._get_product_accounts()
            elif gift_card.buy_line_id:
                accounts = gift_card.buy_line_id.product_id._get_product_accounts()
            else:
                accounts = {}
            if accounts:
                account_move = self.env['account.move'].search([
                    ('ref', 'like', 'GC/%'),
                    ('state', '=', 'draft')
                ], order='id desc', limit=1)
                if account_move:
                    account_move.write({
                        'line_ids': [
                            (0, 0, {
                                'name': gift_card.code,
                                'partner_id': gift_card.partner_id.id if gift_card.partner_id else False,
                                'account_id': accounts['income'].id,  # TODO: Quel compte ?
                                'credit': 0,
                                'debit': gift_card.balance
                            }),
                            (0, 0, {
                                'name': gift_card.code,
                                'partner_id': gift_card.partner_id.id if gift_card.partner_id else False,
                                'account_id': accounts['expired_profit'].id,  # TODO: check if this is correct
                                'credit': gift_card.balance,
                                'debit': 0,
                            }),
                        ]
                    })
                else:
                    self.env['account.move'].create({
                        'ref': self.env['ir.sequence'].next_by_code('gift.card.expired') or '/',
                        'date': fields.Date.today(),
                        'journal_id': accounts['journal'].id,  # TODO: Quel journal ?
                        'line_ids': [
                            (0, 0, {
                                'name': gift_card.code,
                                'partner_id': gift_card.partner_id.id if gift_card.partner_id else False,
                                'account_id': accounts['income'].id,  # TODO: Quel compte ?
                                'credit': 0,
                                'debit': gift_card.balance
                            }),
                            (0, 0, {
                                'name': gift_card.code,
                                'partner_id': gift_card.partner_id.id if gift_card.partner_id else False,
                                'account_id': accounts['expired_profit'].id,  # TODO: check if this is correct
                                'credit': gift_card.balance,
                                'debit': 0,
                            }),
                        ]
                    })
            gift_card.write({'state': 'expired'})
