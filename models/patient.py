from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime, timedelta

class Patient(models.Model):
    _name = "ms_clinic.patient"
    _description = "Patient"
    _rec_name = "name"
    _check_company_auto = True
    _sql_constraints = [
        (
            "identaty_uniq",
            "unique(identaty)",
            "An identaty can only be assigned to one patient!",
        ),
        ("name_uniq", "unique(name)", "A name can only be assigned to one patient!"),
    ]
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        string="Patient Name",
        required=True,
        tracking=True,
    )
    identaty = fields.Char(
        string="Patient Identaty",
        tracking=True,
    )
    birthday = fields.Date(
        string="Birthday",
        tracking=True,
    )
    age = fields.Integer(string="Age")
    gender = fields.Selection(
        [
            ("male", "Male"),
            ("female", "Female"),
        ],
        string="Gender",
        tracking=True,
    )
    address = fields.Text(
        string="Address",
        tracking=True,
    )
    phone = fields.Char(
        string="Phone",
        tracking=True,
    )
    email = fields.Char(
        string="Email",
        tracking=True,
    )
    medical_history_id = fields.Many2many(
        "ms_clinic.medicalhistory",
        string="Medical History",
        tracking=True,
    )
    clinic_id = fields.Many2many(
        "ms_clinic.clinic",
        string="Clinic",
        tracking=True,
    )
    appointments = fields.One2many(
        "ms_clinic.appointment",
        "patient_id",
        string="Appointments",
        tracking=True,
    )
    insurance_id = fields.Many2one(
        "ms_clinic.insurance",
        string="Patient Insurance",
        tracking=True,
    )
