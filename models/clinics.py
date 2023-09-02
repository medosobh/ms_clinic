from odoo import models, fields


class Clinics(models.Model):
    _name = "hospital.clinics"
    _description = "Clinic or Section"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        string="Name", required=True)
    type = fields.Many2one(
        comodel_name="hospital.clinic.type",
        string="Type")
    location = fields.Text(string="Description")
    address = fields.Text(string="Address")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    # tickets_ids = fields.One2many(
    #     comodel_name="hospital.tickets",
    #     inverse_name="clinics_id",
    #     string="Appointments")
    fees_rate = fields.Monetary(
        string="Fees Rate",
        currency_field="currency_id")
    # patients_ids = fields.One2many(
    #     comodel_name='hospital.patients',
    #     inverse_name='clinics_id',
    #     string="Patients")
    # staff_ids = fields.One2many(
    #     comodel_name='hospital.staff',
    #     inverse_name='clinics_id',
    #     string="Staff")
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        change_default=True,
        default=lambda self: self.env.company,
        required=False,
        readonly=True)
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        related='company_id.currency_id',
        readonly=True,
        help="Used to display the currency when tracking monetary values")
    active = fields.Boolean(
        string="Active",
        default=True,
        tracking=True)


class ClinicType(models.Model):
    _name = "hospital.clinic.type"
    _description = "Clinic or Section"

    name = fields.Char(string="Name", required=True)



