# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class WebsiteWithdrawal(models.Model):
    _inherit = 'sale.order'

    picking_type_id = fields.Many2one('stock.picking.type', 'Operation Type')
