from odoo import fields, models, api


class Rooms(models.Model):
    _name = 'hospital.rooms'
    _description = 'Rooms and Beds'

    name = fields.Char()
