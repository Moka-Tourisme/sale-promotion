# -*- coding: utf-8 -*-
{
    'name': 'Gift Card Design',
    'version': '1',
    'category': 'Custom',
    'summary': 'Gift card design',
    'description': "Gift card design",
    'depends': ['product', 'gift_card', 'pos_gift_card'],
    'data': [
        'views/gift_card_design_templates.xml',
        "reports/gift_card_custom_template.xml",
        'data/gift_card_data.xml',
        'data/mail_template_data.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'AGPL-3',
}
