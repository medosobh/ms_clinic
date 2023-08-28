from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime, timedelta


class Staff(models.Model):
    _name = "hospital.staff"
    _description = "Information about staff"

    name = fields.Char(
        string="Name",
        required=True)
    roles_id = fields.Many2one(
        "hospital.role",
        string="Role")
    age = fields.Integer(
        string="Age")
    gender = fields.Selection(
        [
            ("male", "Male"),
            ("female", "Female")
        ], string="Gender")
    phone = fields.Char(
        string="Phone")
    email = fields.Char(
        string="Email")
    contact_number = fields.Char(
        string="Contact Number")
    address = fields.Char(
        string="Address")
    is_active = fields.Boolean(
        string="Active",
        default=True)
    specialization = fields.Char(
        string="Specialization")
    appointments = fields.One2many(
        "hospital.appointments",
        "staff_id",
        string="Appointments")
    clinics_id = fields.Many2many(
        "hospital.clinics",
        string="Clinic")

    def toggle_active(self):
        for record in self:
            record.is_active = True

    def toggle_inactive(self):
        for record in self:
            record.is_active = False


class Roles(models.Model):
    _name = "hospital.roles"
    _description = "Job Roles"
