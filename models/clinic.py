from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime, timedelta

class Clinic(models.Model):
    _name = "ms_hospital.clinic"
    _description = "Clinic or Section"

    name = fields.Char(string="Name", required=True)
    type = fields.Many2one("ms_hospital.clinicttype", "Type")
    location = fields.Text(string="Description")
    address = fields.Text(string="Address")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    website = fields.Char(string="Website")
    appointments = fields.One2many(
        "ms_hospital.appointment", "clinic_id", string="Appointments"
    )
    doctors = fields.Many2many("ms_hospital.doctor", string="Doctors")
    patients = fields.Many2many("ms_hospital.patient", string="Patients")
    pharmacies = fields.Many2many("ms_hospital.pharmacist", string="Pharmacies")
    transactions = fields.One2many(
        "ms_hospital.transaction", "clinic_id", string="Transactions"
    )

    is_active = fields.Boolean(string="Active", default=True)


class ClinicType(models.Model):
    _name = "ms_hospital.clinictype"
    _description = "Clinic or Section"

    name = fields.Char(string="Name", required=True)
