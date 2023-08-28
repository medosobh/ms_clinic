from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime, timedelta


class Staff(models.Model):
    _name = "ms_clinic.staff"
    _description = "Information about staff"

    name = fields.Char(string="Name", required=True)
    title = fields.Many2one("ms_hospital.title", string="Title")
    age = fields.Integer(string="Age")
    gender = fields.Selection([("male", "Male"), ("female", "Female")], string="Gender")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    contact_number = fields.Char(string="Contact Number")
    address = fields.Char(string="Address")
    role = fields.Selection(
        [
            ("receptionist", "Receptionist"),
            ("nurse", "Nurse"),
            ("administrator", "Administrator"),
        ],
        string="Role",
    )
    is_active = fields.Boolean(string="Active", default=True)
    specialization = fields.Char(string="Specialization")
    appointments = fields.One2many(
        "ms_clinic.appointment", "staff_id", string="Appointments"
    )
    clinic_id = fields.Many2many("clinic", string="Clinic")

    def toggle_active(self):
        for record in self:
            record.is_active = True

    def toggle_inactive(self):
        for record in self:
            record.is_active = False


class Title(models.Model):
    _name = "ms_clinic.title"
    _description = "Job Title"
