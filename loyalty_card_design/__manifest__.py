# Copyright 2024 Moka - Horvat Damien
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Loyalty Card Design',
    'summary': 'Allows to design different gift card models and to generate them in PDF format',
    'version': '16.0.0.0.1',
    'category': 'Sale',
    "author": "Moka",
    "website": "https://www.mokatourisme.fr",
    'depends': ['product', 'loyalty', 'pos_loyalty'],
    'data': [
        'data/paperformat_data.xml',
        'report/loyalty_card_custom_template.xml',
        'views/loyalty_program_views.xml',
        'wizard/loyalty_generate_wizard_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'AGPL-3',
}
