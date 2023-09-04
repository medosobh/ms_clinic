from datetime import date

from odoo import models, fields, api


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

    @api.depends('birthday')
    def _get_age(self):
        self.ensure_one()
        if not self.birthday:
            self.age = 0
        else:
            self.age = (date.today().year - self.birthday.year)
        return self.age

    name = fields.Char(
        string="Name",
        required=True,
        tracking=True)
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Partner")
    identity = fields.Char(
        string="Identity",
        tracking=True)
    birthday = fields.Date(
        string="Birthday",
        tracking=True)
    age = fields.Integer(
        string="Age",
        compute='_get_age')
    gender = fields.Selection(
        selection=[
            ("male", "Male"),
            ("female", "Female"),
        ],
        string="Gender",
        tracking=True)
    address = fields.Text(
        string="Address",
        tracking=True)
    phone = fields.Char(
        string="Phone",
        tracking=True)
    email = fields.Char(
        string="Email",
        tracking=True)
    tickets_ids = fields.One2many(
        comodel_name="hospital.tickets",
        inverse_name="patients_id",
        string="Medical History")

    # clinics_ids = fields.One2many(
    #     comodel_name="hospital.clinics",
    #     inverse_name="patients_id",
    #     string="Clinic")

    # insurance_id = fields.Many2one(
    #     comodel_name="hospital.insurance",
    #     string="Patient Insurance",
    #     tracking=True)


class Insurance(models.Model):
    _name = "hospital.insurance"
    _description = "Patient"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        string="Patient Name",
        required=True,
        tracking=True)
