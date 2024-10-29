from datetime import timedelta, datetime

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, UserError


class Rooms(models.Model):
    _name = "hospital.rooms"
    _description = "Rooms and Beds"
    _check_company_auto = True
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        string="Name", required=True)
    type = fields.Many2one(
        comodel_name="hospital.room.type",
        string="Type")
    location = fields.Text(string="Description")
    address = fields.Text(string="Address")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    fees_rate = fields.Monetary(
        string="Fees Rate",
        currency_field="currency_id")
    room_tickets_ids = fields.One2many(
        comodel_name="hospital.room.tickets",
        inverse_name="rooms_id",
        string="Tickets")
    tickets_count = fields.Integer(
        string="Tickets Count",
        compute='_compute_tickets_count')
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        change_default=True,
        default=lambda self: self.env.company,
        required=False,
        readonly=True)
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        related='company_id.currency_id',
        readonly=True,
        help="Used to display the currency when tracking monetary values")
    active = fields.Boolean(
        string="Active",
        default=True,
        tracking=True)

    def _compute_tickets_count(self):
        for rec in self:
            tickets_count = self.env['hospital.room.tickets'].search_count([
                ('rooms_id', '=', rec.id)
            ])
            rec.tickets_count = tickets_count

    def object_open_room_tickets_timeframe(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Orders',
            'res_model': 'hospital.room.tickets',
            'domain': [('rooms_id', '=', self.id)],
            'view_mode': 'calendar,tree,form',
            'target': 'new'
        }


class RoomType(models.Model):
    _name = "hospital.room.type"
    _description = "Rooms and Beds type"
    _check_company_auto = True
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        string="Name",
        required=True)
    bed_num = fields.Integer(
        string="Number of beds",
        required=True,
        tracking=True)
    active = fields.Boolean(
        string="Active",
        default=True,
        tracking=True)



