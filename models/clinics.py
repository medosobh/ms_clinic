from odoo import models, fields


class Clinics(models.Model):
    _name = "hospital.clinics"
    _description = "Clinic or Section"

    name = fields.Char(
        string="Name", required=True)
    type = fields.Many2one(
        comodel_name="hospital.clinic.type", string="Type")
    location = fields.Text(string="Description")
    address = fields.Text(string="Address")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    website = fields.Char(string="Website")
    appointments = fields.One2many(
        comodel_name="hospital.appointments", inverse_name="clinic_id",
        string="Appointments")
    doctors = fields.Many2many(
        comodel_name="hospital.staff",
        string="Doctors")
    patients = fields.Many2many(
        comodel_name="hospital.patients",
        string="Patients")
    pharmacies = fields.Many2many(comodel_name="hospital.staff",
                                  string="Pharmacies")
    is_active = fields.Boolean(string="Active", default=True)


class ClinicType(models.Model):
    _name = "hospital.clinic.type"
    _description = "Clinic or Section"

    name = fields.Char(string="Name", required=True)
