# -*- coding: utf-8 -*-
{
    'name': 'Gift Card Design',
    'version': '1.0.2',
    'category': 'Custom',
    "author": "Moka Tourisme",
    "website": "https://www.mokatourisme.fr",
    'summary': 'Gift card design',
    'description': "Gift card design",
    'depends': ['product', 'gift_card', 'pos_gift_card'],
    'data': [
        "reports/gift_card_custom_template.xml",
        'data/gift_card_data.xml',
        'data/mail_template_data.xml',
        'views/gift_card_design_templates.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'AGPL-3',
}
