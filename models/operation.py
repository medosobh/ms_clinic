from odoo import fields, models, api


class Operations(models.Model):
    _name = 'hospital.operations'
    _description = 'Description'

    name = fields.Char()
