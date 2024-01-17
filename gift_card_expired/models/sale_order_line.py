from odoo import fields, models, api, _

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _build_gift_card(self):
        gift_card = super()._build_gift_card()
        gift_card.update({
            'expired_profit_account': self.product_id.expired_profit_account.id,
        })
        return gift_card