from odoo import api, fields, models

class LoyaltyCard(models.Model):
    _inherit = 'loyalty.card'

    used_by_cron = fields.Boolean(string='Used by cron', default=False)

    def _cron_gift_card_expired(self):
        gift_card_expired_with_balance = self.env['loyalty.card'].search([
            ('expiration_date', '<=', fields.Date.today()), ('points', '>', 0), ('used_by_cron', '=', False)
        ]).filtered(lambda x: x.program_id.trigger_product_ids and len(x.program_id.trigger_product_ids) == 1)
        gift_card_to_expire = self.env['loyalty.card'].search([
            ('expiration_date', '=', fields.Date.today()), ('points', '>', 0),
            ('used_by_cron', '=', False)
        ]).filtered(lambda x: x.program_id.trigger_product_ids and len(x.program_id.trigger_product_ids) == 1)
        print("gift_card_to_expire", gift_card_to_expire)
        if gift_card_expired_with_balance:
            self._create_update_account_move_line(gift_card_expired_with_balance)
        if gift_card_to_expire:
            self._create_update_account_move_line(gift_card_to_expire)

    def _create_update_account_move_line(self, gift_cards):
        for gift_card in gift_cards:
            if gift_card.points > 0:
                expired_date_year = fields.Date.from_string(gift_card.expiration_date).year
                # Create a variable named first_date_year that is like expired_date_year but with the first day of the year
                first_date_year = fields.Date.from_string(gift_card.expiration_date).replace(month=1, day=1)
                # Create a variable named last_date_year that is like expired_date_year but with the last day of the year
                last_date_year = fields.Date.from_string(gift_card.expiration_date).replace(month=12, day=31)
                if gift_card.program_id.trigger_product_ids:
                    accounts = gift_card.program_id.trigger_product_ids[0]._get_product_accounts()
                    print('accounts', accounts)
                else:
                    accounts = {}
                if accounts and accounts['expired_profit'] and accounts['income']:
                    account_move = self.env['account.move'].search([
                        ('ref', 'like', 'GC/%'),
                        ('state', '=', 'draft'),
                        ('date', '>=', first_date_year),
                        ('date', '<=', last_date_year)
                    ], order='id desc', limit=1)
                    if account_move:
                        print("GIFT CARD BALANCE", gift_card.points)
                        account_move.write({
                            'line_ids': [
                                (0, 0, {
                                    'name': gift_card.code,
                                    'partner_id': gift_card.partner_id.id if gift_card.partner_id else False,
                                    'account_id': accounts['income'].id,  # TODO: Quel compte ?
                                    'credit': 0,
                                    'debit': gift_card.points,
                                }),
                                (0, 0, {
                                    'name': gift_card.code,
                                    'partner_id': gift_card.partner_id.id if gift_card.partner_id else False,
                                    'account_id': accounts['expired_profit'].id,  # TODO: check if this is correct
                                    'credit': gift_card.points,
                                    'debit': 0,
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
                                    'debit': gift_card.points,
                                }),
                                (0, 0, {
                                    'name': gift_card.code,
                                    'partner_id': gift_card.partner_id.id if gift_card.partner_id else False,
                                    'account_id': accounts['expired_profit'].id,  # TODO: check if this is correct
                                    'credit': gift_card.points,
                                    'debit': 0,
                                }),
                            ]
                        })
                    gift_card.write({'used_by_cron': True})
