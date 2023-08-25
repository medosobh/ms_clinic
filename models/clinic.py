from odoo import models, fields, api


class Clinic(models.Model):
    _name = 'ms_clinic.clinic'
    _description = 'Clinic or Section'

    name = fields.Char(
        string='Name',
        required=True
    )
    location = fields.Text(
        string='Description'
    )
    address = fields.Text(
        string='Address'
    )
    phone = fields.Char(
        string='Phone'
    )
    email = fields.Char(
        string='Email'
    )
    website = fields.Char(
        string='Website'
    )
    doctors = fields.Many2many(
        'ms_clinic.doctor',
        string='Doctors'
    )
    patients = fields.One2many(
        'ms_clinic.patient',
        'clinic_id', string='Patients'
    )
    pharmacies = fields.One2many(
        'ms_clinic.pharmacist',
        'clinic_id',
        string='Pharmacies'
    )
    transactions = fields.One2many(
        'ms_clinic.transaction',
        'clinic_id',
        string='Transactions'
    )
    appointments = fields.One2many(
        'ms_clinic.appointment',
        'clinic_id',
        string='Appointments'
    )
    is_active = fields.Boolean(
        string='Active',
        default=True
    )
