from odoo import fields, models, api


class MedicalSupplies(models.Model):
    _name = 'hospital.medical.supplies'
    _description = 'Medical Supplies'

    name = fields.Char()
