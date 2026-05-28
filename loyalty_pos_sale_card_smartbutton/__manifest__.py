# Copyright 2025 Moka
# @author Horvat Damien <damien@moka.cloud>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Loyalty Pos Sale Card Smartbutton",
    "summary": "Add a smart button on pos orders to show gift cards",
    "version": "16.0.1.0.0",
    "author": "Moka",
    "website": "https://moka.cloud",
    "license": "AGPL-3",
    "category": "Loyalty",
    "depends": ["pos_sale_loyalty"],
    "data": [
        'views/pos_order_views.xml',
        "views/loyalty_card_views.xml",
    ],
    "auto-install": False,
}
