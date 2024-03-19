from odoo import api, fields, models


class Giftcard(models.Model):
    _inherit = 'gift.card'

    expired_profit_account = fields.Many2one('account.account', string='Expired Profit Account',
                                             help="Account used to record the expired profit of the gift card.")

    def _cron_gift_card_expired(self):
        gift_card_expired_with_balance = self.env['gift.card'].search([
            ('state', '=', 'expired'), ('balance', '>', 0)
        ])
        gift_card_to_expire = self.env['gift.card'].search([
            ('state', '=', 'valid'), ('expired_date', '<', fields.Date.today()), ('balance', '>', 0)
        ])
        if gift_card_expired_with_balance:
            self._create_update_account_move_line(gift_card_expired_with_balance)
        if gift_card_to_expire:
            self._create_update_account_move_line(gift_card_to_expire)

    def _create_update_account_move_line(self, gift_cards):
        for gift_card in gift_cards:
            expired_date_year = fields.Date.from_string(gift_card.expired_date).year
            # Create a variable named first_date_year that is like expired_date_year but with the first day of the year
            first_date_year = fields.Date.from_string(gift_card.expired_date).replace(month=1, day=1)
            # Create a variable named last_date_year that is like expired_date_year but with the last day of the year
            last_date_year = fields.Date.from_string(gift_card.expired_date).replace(month=12, day=31)
            if gift_card.buy_pos_order_line_id:
                accounts = gift_card.buy_pos_order_line_id.product_id._get_product_accounts()
            elif gift_card.buy_line_id:
                accounts = gift_card.buy_line_id.product_id._get_product_accounts()
            else:
                accounts = {}
            if accounts:
                account_move = self.env['account.move'].search([
                    ('ref', 'like', 'GC/%'),
                    ('state', '=', 'draft'),
                    ('date', '>=', first_date_year),
                    ('date', '<=', last_date_year)
                ], order='id desc', limit=1)
                print("account_move", account_move)
                if account_move:
                    account_move.write({
                        'line_ids': [
                            (0, 0, {
                                'name': gift_card.code,
                                'partner_id': gift_card.partner_id.id if gift_card.partner_id else False,
                                'account_id': accounts['income'].id,  # TODO: Quel compte ?
                                'credit': 0,
                                'debit': gift_card.balance,
                                'currency_id': self.env.company.currency_id.id,
                            }),
                            (0, 0, {
                                'name': gift_card.code,
                                'partner_id': gift_card.partner_id.id if gift_card.partner_id else False,
                                'account_id': accounts['expired_profit'].id,  # TODO: check if this is correct
                                'credit': gift_card.balance,
                                'debit': 0,
                                'currency_id': self.env.company.currency_id.id,
                            }),
                        ]
                    })
                else:
                    self.env['account.move'].create({
                        'ref': self.env['ir.sequence'].next_by_code('gift.card.expired') or '/',
                        'date': gift_card.expired_date,
                        'journal_id': accounts['journal'].id,  # TODO: Quel journal ?
                        'line_ids': [
                            (0, 0, {
                                'name': gift_card.code,
                                'partner_id': gift_card.partner_id.id if gift_card.partner_id else False,
                                'account_id': accounts['income'].id,  # TODO: Quel compte ?
                                'credit': 0,
                                'debit': gift_card.balance,
                                'currency_id': self.env.company.currency_id.id,
                            }),
                            (0, 0, {
                                'name': gift_card.code,
                                'partner_id': gift_card.partner_id.id if gift_card.partner_id else False,
                                'account_id': accounts['expired_profit'].id,  # TODO: check if this is correct
                                'credit': gift_card.balance,
                                'debit': 0,
                                'currency_id': self.env.company.currency_id.id,
                            }),
                        ]
                    })
                gift_card.write({'state': 'expired'})
