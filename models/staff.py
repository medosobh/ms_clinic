from datetime import date

from odoo import models, fields, api


class Staff(models.Model):
    _name = "hospital.staff"
    _description = "Staff"
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
        required=True)
    roles_id = fields.Many2one(
        comodel_name="hospital.roles",
        string="Role")
    birthday = fields.Date(
        string="Birthday",
        tracking=True)
    age = fields.Integer(
        string="Age",
        compute='_get_age')
    gender = fields.Selection(
        selection=[
            ("male", "Male"),
            ("female", "Female")
        ], string="Gender")
    phone = fields.Char(
        string="Phone")
    email = fields.Char(
        string="Email")
    address = fields.Char(
        string="Address")
    active = fields.Boolean(
        string="Active",
        default=True)
    specialization = fields.Char(
        string="Specialization")
    # tickets_ids = fields.One2many(
    #     comodel_name="hospital.tickets",
    #     inverse_name="staff_id",
    #     string="Appointments")
    # clinics_id = fields.Many2many(
    #     comodel_name="hospital.clinics",
    #     string="Clinic")


class Roles(models.Model):
    _name = "hospital.roles"
    _description = "Staff Roles"
