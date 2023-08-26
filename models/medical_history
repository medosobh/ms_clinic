from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta
from odoo.modules.module import get_module_resource
import base64

class medicalhistory(models.Model):

    _name = 'ms_clinic.medicalhistory'
    _description = 'Medical History'
    _rec_name = 'code'
    _check_company_auto = True
    _sql_constraints = [
        ('code_uniq', 'unique(code)', "A code can only be assigned to one Maid!"),
    ]
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    
    code = fields.Char(
        string='Code'
    )