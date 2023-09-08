from odoo import fields, models, api


class Pharmacy(models.Model):
    _name = 'hospital.pharmacy'
    _description = 'Description'

    name = fields.Char()
