# Copyright 2022 Moka Tourisme (https://www.mokatourisme.fr).
# @author Romain DUCIEL<romain@mokatourisme.fr>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _send_gift_card_mail(self):
        template = self.env.ref('compagniedudragon.mail_template_gift_card_custom', raise_if_not_found=False)
        if template and self.gift_card_count:
            for gift in self.order_line.mapped("generated_gift_card_ids"):
                template.send_mail(gift.id, force_send=True, notif_layout='mail.mail_notification_light')
