from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime, timedelta

class Service(models.Model):
    _name = 'ms_hospital.service'
    _description = 'ms_hospital.service'
    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(
        string='Name',
        required=True,
        copy=False
    )


    

    

