# Copyright 2022 Moka Tourisme (https://www.mokatourisme.fr).
# @author Romain DUCIEL<romain@mokatourisme.fr>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
import base64


class PosOrder(models.Model):
    _inherit = "pos.order"
    def _add_mail_attachment(self, name, ticket):
        attachment = super()._add_mail_attachment(name, ticket)
        self.ensure_one()
        if self.config_id.use_gift_card and len(self.get_new_card_ids()) > 0:
            report = self.env.ref('compagniedudragon.gift_card_custom_report')._render_qweb_pdf(self.get_new_card_ids())
            filename = name + '.pdf'
            gift_card = self.env['ir.attachment'].create({
                'name': filename,
                'type': 'binary',
                'datas': base64.b64encode(report[0]),
                'store_fname': filename,
                'res_model': 'pos.order',
                'res_id': self.id,
                'mimetype': 'application/x-pdf'
            })
            attachment += [(4, gift_card.id)]

        return attachment
