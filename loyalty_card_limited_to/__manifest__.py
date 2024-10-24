# Copyright 2024 Moka - Horvat Damien
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Loyalty Card Limited To',
    'version': '18.0.1.0.0',
    'author' : 'Moka',
    "website": "https://www.moka.cloud",
    'description' : "Limit loyalty card on specific products",
    'category': 'Sales',
    "license": "AGPL-3",
    'summary': 'Custom gift card limitation',
    'depends': ['loyalty', 'pos_loyalty', 'sale_loyalty'],
    'data': [
        'views/loyalty_card_reward_views_inherit.xml',
        'views/loyalty_card_views_inherit.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}