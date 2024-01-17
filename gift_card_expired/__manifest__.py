# Copyright 2023 MokaTourisme (https://www.mokatourisme.fr)
# @author Romain Duciel <romain@mokatourisme.fr>

{
    "name": "Gift Card Expired",
    "summary": "Set the balance of the gift card to another account when it expires",
    "author": "Mokatourisme",
    "version": "15.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["gift_card", "pos_gift_card", "sale_gift_card", "l10n_fr"],
    "data": [
        "views/product_template.xml",
        "data/gift_card_expired_cron.xml",
        "data/gift_card_sequence.xml",
    ],
}
