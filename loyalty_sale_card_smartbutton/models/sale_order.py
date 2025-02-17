from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    loyalty_card_count = fields.Integer(
        string="Loyalty Cards Count",
        compute="_compute_loyalty_card_count",
        store=False 
    )

    def _compute_loyalty_card_count(self):
        """
        Count the loyalty cards associated with this sale order.
        """
        for order in self:
            cards = self.env['loyalty.card'].search([('order_id', '=', order.id)])
            order.loyalty_card_count = len(cards)

    def action_open_loyalty_cards(self):
        """
        Ouvre une vue d'action affichant toutes les cartes liées à cette sale.order.
        """
        self.ensure_one()
        # Recherche des cartes associées à la commande en cours
        loyalty_cards = self.env['loyalty.card'].search([('order_id', '=', self.id)])
        if not loyalty_cards:
            return {
                'type': 'ir.actions.act_window_close'
            }
        action = self.env.ref('loyalty_sale_card_smartbutton.action_loyalty_cards_from_sale_order').read()[0]
        action.update({
            'domain': [('id', 'in', loyalty_cards.ids)],
            'context': {'default_order_id': self.id},
        })
        return action
    
