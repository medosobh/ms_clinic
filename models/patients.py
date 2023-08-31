from odoo import models, fields


class Patients(models.Model):
    _name = "hospital.patients"
    _description = "Patient"
    _rec_name = "name"
    _check_company_auto = True
    _sql_constraints = [
        (
            "identity_uniq",
            "unique(identity)",
            "An identity can only be assigned to one patient!",
        ),
        ("name_uniq", "unique(name)",
         "A name can only be assigned to one patient!"),
    ]
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        string="Patient Name",
        required=True,
        tracking=True,
    )
    identity = fields.Char(
        string="Patient Identity",
        tracking=True,
    )
    birthday = fields.Date(
        string="Birthday",
        tracking=True,
    )
    age = fields.Integer(string="Age")
    gender = fields.Selection(
        selection=[
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
        comodel_name="hospital.medical.history",
        string="Medical History",
        tracking=True,
    )
    clinics_id = fields.One2many(
        comodel_name="hospital.clinics",
        inverse_name="patients_id",
        string="Clinic",
        tracking=True)
    appointments = fields.One2many(
        comodel_name="hospital.appointments",
        inverse_name="patient_id",
        string="Appointments",
        tracking=True)
    insurance_id = fields.Many2one(
        comodel_name="hospital.insurance",
        string="Patient Insurance",
        tracking=True)


class Insurance(models.Model):
    _name = "hospital.insurance"
    _description = "Patient"

    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        string="Patient Name",
        required=True,
        tracking=True,
    )
