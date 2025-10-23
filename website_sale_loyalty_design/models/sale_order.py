from odoo import models, fields, api
from datetime import timedelta
import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    gift_card_gifter_name = fields.Char(string="Gifter Name")
    gift_card_recipient_name = fields.Char(string="Recipient Name")
    gift_card_occasion = fields.Char(string="Occasion")

    def _delayed_update_gift_cards(self):
        """Method called by cron or manually with delay"""
        orders_to_update = self.search([
            ('state', 'in', ['sale', 'done']),
            ('create_date', '>=', fields.Datetime.now() - timedelta(hours=1)),
            '|', ('gift_card_gifter_name', '!=', False),
            '|', ('gift_card_recipient_name', '!=', False),
            ('gift_card_occasion', '!=', False)
        ])
        
        for order in orders_to_update:
            if order._has_gift_card_product():
                updated = order._update_gift_cards_custom_fields()
                _logger.info(f"Delayed update for order {order.id}: {updated} cards updated")

    def action_confirm(self):
        """Override to set custom fields on gift cards after confirmation"""
        result = super().action_confirm()
        
        if self._has_gift_card_product():
            updated_count = self._update_gift_cards_custom_fields()
            
            if updated_count == 0:
                self.env['ir.cron'].sudo().search([
                    ('model_id.model', '=', 'sale.order'),
                    ('name', 'ilike', 'Update Gift Cards')
                ], limit=1)._trigger(at=self.id)
        
        return result
    
    def _update_gift_cards_custom_fields(self):
        """Update gift cards with custom fields from the sale order"""
        if not (self.gift_card_gifter_name or self.gift_card_recipient_name or self.gift_card_occasion):
            return
            
        _logger.info(f"Updating gift cards for order {self.id} with partner {self.partner_id.id}")
        
        recent_cards = self._get_recent_gift_cards()
        
        if not recent_cards:
            recent_cards = self._get_recent_gift_cards_extended()
            
        _logger.info(f"Found {len(recent_cards)} recent gift cards")
        
        updated_cards = 0
        for card in recent_cards:
            if self._is_gift_card_from_order(card):
                card.write({
                    'gifter_name': self.gift_card_gifter_name,
                    'recipient_name': self.gift_card_recipient_name,
                    'occasion': self.gift_card_occasion,
                })
                updated_cards += 1
                _logger.info(f"Updated gift card {card.id} with custom fields")
        
        _logger.info(f"Updated {updated_cards} gift cards for order {self.id}")
        return updated_cards
    
    def _get_recent_gift_cards(self):
        """Get recent gift cards for this partner"""
        return self.env['loyalty.card'].search([
            ('partner_id', '=', self.partner_id.id),
            ('program_id.program_type', '=', 'gift_card'),
            ('source_pos_order_id', '=', False),
            ('create_date', '>=', self.create_date - timedelta(minutes=5)),
            ('create_date', '<=', fields.Datetime.now()),
        ])
    
    def _get_recent_gift_cards_extended(self):
        """Get recent gift cards with extended search"""
        gift_amounts = [line.price_unit for line in self.order_line if self._line_has_gift_card(line)]
        
        if not gift_amounts:
            return self.env['loyalty.card']
            
        domain = [
            ('program_id.program_type', '=', 'gift_card'),
            ('source_pos_order_id', '=', False),
            ('create_date', '>=', self.create_date - timedelta(minutes=10)),
            ('create_date', '<=', fields.Datetime.now()),
            ('points', 'in', gift_amounts),
        ]
        
        return self.env['loyalty.card'].search(domain)
    
    def _line_has_gift_card(self, line):
        """Check if a line contains a gift card product"""
        gift_programs = self.env['loyalty.program'].search([('program_type', '=', 'gift_card')])
        return any(line.product_id in program.trigger_product_ids for program in gift_programs)
    
    def _is_gift_card_from_order(self, card):
        """Check if a gift card corresponds to this order - Version améliorée"""
        for line in self.order_line:
            if not self._line_has_gift_card(line):
                continue
                
            if abs(card.points - line.price_unit) < 0.01:
                gift_programs = self.env['loyalty.program'].search([
                    ('program_type', '=', 'gift_card'),
                    ('trigger_product_ids', 'in', line.product_id.id)
                ])
                
                if card.program_id in gift_programs:
                    if not (card.gifter_name or card.recipient_name or card.occasion):
                        return True
        return False
    
    def _has_gift_card_product(self):
        """Check if the order contains a gift card product"""
        return any(self._line_has_gift_card(line) for line in self.order_line)

    @api.model
    def _get_gift_card_programs(self):
        """Get available gift card programs for website"""
        return self.env['loyalty.program'].search([
            ('program_type', '=', 'gift_card'),
            ('active', '=', True)
        ])
