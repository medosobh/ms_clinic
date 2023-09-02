from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime, timedelta


class Staff(models.Model):
    _name = "hospital.staff"
    _description = "Information about staff"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        string="Name",
        required=True)
    roles_id = fields.Many2one(
        comodel_name="hospital.roles",
        string="Role")
    age = fields.Integer(
        string="Age")
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

    def toggle_active(self):
        for record in self:
            record.is_active = True

    def toggle_inactive(self):
        for record in self:
            record.is_active = False


class Roles(models.Model):
    _name = "hospital.roles"
    _description = "Staff Roles"
