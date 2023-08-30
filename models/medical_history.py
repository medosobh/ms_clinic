from odoo import fields, models


class MedicalHistory(models.Model):
    _name = 'hospital.medical.history'
    _description = 'Medical History'
    _rec_name = 'code'
    _check_company_auto = True
    _sql_constraints = [
        ('code_uniq', 'unique(code)',
         "A code can only be assigned to one Maid!"),
    ]
    _inherit = ['mail.thread', 'mail.activity.mixin']

    code = fields.Char(string='Code')
