from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers import main
import json
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleLoyaltyDesign(main.WebsiteSale):

    @http.route()
    def cart_update_json(self, **kwargs):
        """Override pour gérer l'ajout automatique de la carte cadeau physique"""
        print("=== DEBUT cart_update_json override ===")
        print(f"Kwargs reçus: {kwargs}")
        
        result = super().cart_update_json(**kwargs)
        
        print("=== Méthode parent appelée ===")
        
        try:
            product_id = kwargs.get('product_id')
            add_qty = kwargs.get('add_qty')
            
            if product_id and add_qty and int(add_qty) > 0:
                product = request.env['product.product'].browse(int(product_id))
                print(f"Produit trouvé: {product.name}")
                
                if self._is_gift_card_product(product):
                    print("=== C'est une carte cadeau ! ===")
                    self._handle_gift_card_addition(product, **kwargs)
                    
        except Exception as e:
            print(f"Erreur dans la logique custom: {e}")
        
        print("=== FIN cart_update_json override ===")
        return result

    @http.route(['/shop/cart/update_gift_info'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def cart_update_gift_info(self, **kw):
        """Update gift card information on current order"""
        order = request.website.sale_get_order()
        
        if not order:
            return {'error': 'No active order found'}
            
        if not self._order_has_gift_card(order):
            return {'error': 'No gift card in order'}
            
        gift_card_data = {}
        allowed_fields = [
            'gift_card_gifter_name',
            'gift_card_recipient_name', 
            'gift_card_occasion',
        ]
        
        for field in allowed_fields:
            if field in kw:
                gift_card_data[field] = kw[field]
        
        if gift_card_data:
            order.sudo().write(gift_card_data)

        return {'success': True, 'message': 'Gift card information updated'}

    def _order_has_gift_card(self, order):
        """Check if order contains gift card products/programs"""
        for line in order.order_line:
            if hasattr(line, 'reward_id') and line.reward_id and line.reward_id.program_id.program_type == 'gift_card':
                return True
        
        for line in order.order_line:
            if self._is_gift_card_product(line.product_id):
                return True
                
        return False

    def _is_gift_card_product(self, product):
        """Vérifier si le produit est une carte cadeau"""
        print(f"Vérification si {product.name} est une carte cadeau")
        
        gift_card_programs = request.env['loyalty.program'].sudo().search([
            ('program_type', '=', 'gift_card')
        ])
        
        for program in gift_card_programs:
            for rule in program.rule_ids:
                if product in rule.product_ids:
                    print(f"Produit trouvé dans le programme {program.name}")
                    return True
        
        if hasattr(product, 'is_gift_card') and product.is_gift_card:
            print("Produit marqué comme carte cadeau")
            return True
            
        gift_card_keywords = ['gift', 'cadeau', 'carte']
        product_name_lower = product.name.lower()
        
        for keyword in gift_card_keywords:
            if keyword in product_name_lower:
                print(f"Produit détecté comme carte cadeau par mot-clé: {keyword}")
                return True
                
        print("Produit n'est pas une carte cadeau")
        return False

    def _handle_gift_card_addition(self, gift_card_product, **kw):
        """Gérer l'ajout de la carte cadeau physique si nécessaire"""
        print("Gestion de l'ajout de carte cadeau")
        
        gift_card_program = self._get_gift_card_program(gift_card_product)
        
        if not gift_card_program:
            print("Pas de programme de carte cadeau trouvé")
            return
        else:
            print(f"Programme de carte cadeau trouvé: {gift_card_program.name}")
            self._add_physical_gift_card(gift_card_program)

    def _get_gift_card_program(self, gift_card_product):
        """Récupérer le programme de carte cadeau pour un produit donné"""
        gift_card_programs = request.env['loyalty.program'].sudo().search([
            ('program_type', '=', 'gift_card')
        ])
        
        for program in gift_card_programs:
            for rule in program.rule_ids:
                if gift_card_product in rule.product_ids:
                    return program
        return None

    def _add_physical_gift_card(self, gift_card_program):
        """Ajouter la carte cadeau physique au panier"""
        print("Tentative d'ajout de carte physique")
        
        if not gift_card_program.physical_gift_card_product_id:
            print("Pas de produit physique configuré")
            return
            
        physical_product = gift_card_program.physical_gift_card_product_id
        print(f"Produit physique à ajouter: {physical_product.name} (ID: {physical_product.id})")
        
        order = request.website.sale_get_order()
        existing_line = order.order_line.filtered(
            lambda line: line.product_id.id == physical_product.id
        )
        
        if not existing_line:
            print("Ajout du produit physique au panier")
            try:
                line_vals = {
                    'product_id': physical_product.id,
                    'product_uom_qty': 1,
                    'product_uom': physical_product.uom_id.id,
                    'order_id': order.id,
                    'name': physical_product.display_name,
                    'price_unit': 0.0,
                    'tax_id': [(6, 0, physical_product.taxes_id.ids)],
                    'sequence': 9999,
                }
                
                print(f"Valeurs de ligne à créer: {line_vals}")
                
                new_line = request.env['sale.order.line'].sudo().create(line_vals)
                print(f"✅ Ligne de produit physique créée avec ID: {new_line.id}")
                
                order.sudo()._recompute_taxes()
                
            except Exception as e:
                print(f"❌ Erreur lors de la création de ligne: {str(e)}")
                
                try:
                    print("Tentative avec approche basique")
                    
                    default_vals = request.env['sale.order.line'].sudo().default_get([
                        'product_id', 'product_uom_qty', 'product_uom', 
                        'name', 'price_unit', 'order_id'
                    ])
                    
                    default_vals.update({
                        'product_id': physical_product.id,
                        'product_uom_qty': 1,
                        'product_uom': physical_product.uom_id.id,
                        'order_id': order.id,
                        'name': f"[OFFERT] {physical_product.display_name}",
                        'price_unit': 0.0,
                    })
                    
                    new_line = request.env['sale.order.line'].sudo().create(default_vals)
                    print(f"✅ Ligne créée avec approche basique: {new_line.id}")
                    
                except Exception as e2:
                    print(f"❌ Erreur avec approche basique: {str(e2)}")
                    
                    try:
                        print("Tentative avec contexte spécial")
                        
                        special_context = dict(request.env.context)
                        special_context.update({
                            'website_sale_loyalty_design': True,
                            'bypass_website_restrictions': True,
                        })
                        
                        line_vals_simple = {
                            'product_id': physical_product.id,
                            'product_uom_qty': 1,
                            'order_id': order.id,
                            'name': physical_product.display_name,
                            'price_unit': 0.0,
                        }
                        
                        new_line = request.env['sale.order.line'].sudo().with_context(special_context).create(line_vals_simple)
                        print(f"✅ Ligne créée avec contexte spécial: {new_line.id}")
                        
                    except Exception as e3:
                        print(f"❌ Toutes les tentatives ont échoué: {str(e3)}")
        else:
            print("Produit physique déjà dans le panier")


    def _remove_physical_gift_card(self, gift_card_program):
        """Retirer la carte cadeau physique du panier"""
        if not gift_card_program.physical_gift_card_product_id:
            return
            
        order = request.website.sale_get_order()
        physical_lines = order.order_line.filtered(
            lambda line: line.product_id.id == gift_card_program.physical_gift_card_product_id.id
        )
        
        if physical_lines:
            physical_lines.unlink()
