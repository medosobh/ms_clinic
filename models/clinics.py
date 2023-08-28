from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime, timedelta

class Clinics(models.Model):
    _name = "hospital.clinics"
    _description = "Clinic or Section"

    name = fields.Char(string="Name", required=True)
    type = fields.Many2one("hospital.clinicttype", "Type")
    location = fields.Text(string="Description")
    address = fields.Text(string="Address")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    website = fields.Char(string="Website")
    appointments = fields.One2many(
        "hospital.appointment", "clinic_id", string="Appointments"
    )
    doctors = fields.Many2many("hospital.doctor", string="Doctors")
    patients = fields.Many2many("hospital.patient", string="Patients")
    pharmacies = fields.Many2many("hospital.pharmacist", string="Pharmacies")
    transactions = fields.One2many(
        "hospital.transaction", "clinic_id", string="Transactions"
    )

    is_active = fields.Boolean(string="Active", default=True)


class ClinicType(models.Model):
    _name = "hospital.clinictype"
    _description = "Clinic or Section"

    name = fields.Char(string="Name", required=True)
