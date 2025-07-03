# Copyright 2023 MokaTourisme (https://www.mokatourisme.fr)
# @author Romain Duciel <romain@mokatourisme.fr>

{
    "name": "Loyalty program Expired",
    "summary": "Set the balance of the gift card to another account when it expires",
    "author": "Mokatourisme",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["loyalty", "pos_sale_loyalty", "sale_loyalty", "l10n_fr", "account"],
    "data": [
        "views/product_template.xml",
        "data/gift_card_expired_cron.xml",
        "data/gift_card_sequence.xml",
    ],
}
