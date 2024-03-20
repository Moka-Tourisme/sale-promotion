{
    'name': 'Gift Card limited to',
    'version': '15.0.1.0.0',
    'author' : 'Moka Tourisme',
    "website": "https://www.mokatourisme.fr",
    'description' : "Limite l'utilisation des cartes cadeaux sur des articles",
    'category': 'Sales',
    "license": "AGPL-3",
    'summary': 'Module de personnalisation des cartes cadeaux',
    'depends': ['gift_card_design', 'pos_gift_card_design', 'sale_gift_card_design'],
    'data': [
        'views/gift_card_view.xml',
        'views/gift_card_design_templates.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}