# Copyright 2024 Moka - Horvat Damien
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Website Sale Loyalty Card Design',
    'summary': '',
    'version': '16.0.0.0.0',
    'category': 'Sale',
    "author": "Moka",
    "website": "https://www.moka.cloud",
    'depends': ['website', 'loyalty', 'loyalty_card_design', 'website_sale_loyalty'],
    'data': [
        'views/website_loyalty_templates.xml',
        'views/loyalty_card_views.xml',
        'data/ir_cron.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'website_sale_loyalty_design/static/src/js/website_sale_loyalty.js',
            # 'website_sale_loyalty_design/static/src/css/website_sale_loyalty.css',
        ],
    },
    'installable': True,
    'auto_install': False,
    'license': 'AGPL-3',
}
