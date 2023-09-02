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

