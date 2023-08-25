from odoo import models, fields, api


class Doctor(models.Model):
    _name = 'ms_clinic.doctor'
    _description = 'Doctor/Practitioner Information'

    name = fields.Char(string='Name', required=True)
    age = fields.Integer(string='Age')    
    specialization = fields.Char(string='Specialization')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string='Gender')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    appointments = fields.One2many('ms_clinic.appointment', 'doctor_id', string='Appointments')
