from odoo import models, fields, api
from datetime import timedelta


class LoyaltyCard(models.Model):
    _inherit = 'loyalty.card'

    gifter_name = fields.Char(
    string="Gifter Name", 
    help="Name of the person offering the gift", 
    required=False)

    recipient_name = fields.Char(
        string="Recipient Name", 
        help="Name of the gift recipient", 
        required=False)

    occasion = fields.Char(
        string="Occasion", 
        help="Occasion for the gift (Christmas, Birthday, etc.)", 
        required=False)

    @api.model_create_multi
    def create(self, vals_list):
        """Override create to set default values from website sale order"""
        for vals in vals_list:
                sale_order = self._get_related_sale_order(vals)
                if sale_order:
                    if sale_order.gift_card_gifter_name:
                        vals['gifter_name'] = sale_order.gift_card_gifter_name
                    if sale_order.gift_card_recipient_name:
                        vals['recipient_name'] = sale_order.gift_card_recipient_name
                    if sale_order.gift_card_occasion:
                        vals['occasion'] = sale_order.gift_card_occasion
        
        return super().create(vals_list)

    def _get_related_sale_order(self, vals):
        """Find the sale order that triggered this gift card creation"""
        if not vals.get('partner_id'):
            return False
            
        sale_orders = self.env['sale.order'].search([
            ('partner_id', '=', vals['partner_id']),
            ('state', 'in', ['sale', 'done']),
            ('create_date', '>=', fields.Datetime.now() - timedelta(minutes=10)),
            '|', ('gift_card_gifter_name', '!=', False),
            '|', ('gift_card_recipient_name', '!=', False),
            ('gift_card_occasion', '!=', False)
        ], order='create_date desc', limit=1)
        
        return sale_orders[0] if sale_orders else False
