from odoo import models, fields


class Services(models.Model):
    _name = 'hospital.services'
    _description = 'Service'
    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(
        string='Name',
        required=True,
        copy=False)
    description = fields.Text(
        string="Description")
    unit_price = fields.Float(
        string="Unit Price")

    def create_service_product(self):
        return
