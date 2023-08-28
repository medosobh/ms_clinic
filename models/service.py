from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime, timedelta


class Services(models.Model):
    _name = 'hospital.services'
    _description = 'hospital.service'
    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(
        string='Name',
        required=True,
        copy=False)
    description = fields.Text(
        string="Description")


# service product
class ProductTemplate(models.Model):
    _inherit = "product.template"
    _description = "Information about medicines"

    service_name = fields.Char(
        string="Service Name",
        required=True)
    description = fields.Text(
        string="Description")
    unit_price = fields.Float(string="Unit Price")
    quantity = fields.Integer(string="Quantity")
    services_id = fields.Many2one('hospital.services',
                                  string="Manufacturer")
