import logging
import psycopg2

from odoo import api, fields, models, registry, SUPERUSER_ID, _

_logger = logging.getLogger(__name__)


class WithdrawalPoints(models.Model):
    _name = "delivery.withdrawal.point"
    _description = "Delivery Withdrawal Point"
    _order = 'sequence, point_id, id'

    # @api.depends('variable', 'operator', 'max_value', 'list_base_price', 'list_price', 'variable_factor')
    # def _compute_name(self):
    #     for rule in self:
    #         name = 'if %s %s %.02f then' % (rule.variable, rule.operator, rule.max_value)
    #         if rule.list_base_price and not rule.list_price:
    #             name = '%s fixed price %.02f' % (name, rule.list_base_price)
    #         elif rule.list_price and not rule.list_base_price:
    #             name = '%s %.02f times %s' % (name, rule.list_price, rule.variable_factor)
    #         else:
    #             name = '%s fixed price %.02f plus %.02f times %s' % (name, rule.list_base_price, rule.list_price, rule.variable_factor)
    #         rule.name = name

    # name = fields.Char(compute='_compute_name')
    sequence = fields.Integer(string='Sequence', default=10)
    point_id = fields.Many2one('delivery.carrier', string='Point reference', required=True, ondelete='cascade',
                               index=True, copy=False)
    partner_id = fields.Many2one('res.partner', 'Address', required=True, domain=[('is_withdrawal', '=', True)])
    resource_calendar_id = fields.Many2one('resource.calendar', 'Working hours', required=True,
                                           domain=[('is_withdrawal_working_time', '=', True)])
    stock_picking_type_id = fields.Many2one('stock.picking.type', 'Stock', required=True, domain=[('code', '=', 'outgoing')])
    opening_hours = fields.Text()

    partner_address_street = fields.Text(compute="_compute_address")
    partner_address_city = fields.Text(compute="_compute_address")
    partner_address_zip = fields.Text(compute="_compute_address")
    partner_country_id = fields.Text(compute="_compute_address")

    @api.onchange('resource_calendar_id')
    def resource_calendar_id_change(self):
        self._updateHours()

    @api.onchange("partner_id")
    def _compute_address(self):
        self.partner_address_street = self.partner_id.street
        self.partner_address_city = self.partner_id.city
        self.partner_address_zip = self.partner_id.zip
        self.partner_country_id = self.partner_id.country_id.id

    def _updateHours(self):
        if not self.resource_calendar_id:
            return
        values = self.resource_calendar_id.attendance_ids
        vals = ""
        for i, val in enumerate(values):
            hour_from = '{0:02.0f}:{1:02.0f}'.format(*divmod(float(val.hour_from) * 60, 60))
            hour_to = '{0:02.0f}:{1:02.0f}'.format(*divmod(float(val.hour_to) * 60, 60))
            if i < (len(values) - 1):
                vals += val.display_name + " from " + str(hour_from) + " to " + str(hour_to) + ", "
            else:
                vals += val.display_name + " from " + str(hour_from) + " to " + str(hour_to)

        self.update({'opening_hours': vals})
