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

    name = fields.Char(
        string="Name",
        required=True,
        tracking=True)
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        required=True,
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
    clinic_tickets_ids = fields.One2many(
        comodel_name="hospital.clinic.tickets",
        inverse_name="patients_id",
        string="Medical History")
    tickets_count = fields.Integer(
        string="Tickets Count",
        compute='_compute_tickets_count')
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

    # insurance_id = fields.Many2one(
    #     comodel_name="hospital.insurance",
    #     string="Patient Insurance",
    #     tracking=True)

    @api.depends('birthday')
    def _get_age(self):
        self.ensure_one()
        if not self.birthday:
            self.age = 0
        else:
            self.age = (date.today().year - self.birthday.year)
        return self.age

    def _compute_tickets_count(self):
        for rec in self:
            tickets_count = self.env['hospital.clinic.tickets'].search_count([
                ('patients_id', '=', rec.id)
            ])
            rec.tickets_count = tickets_count

    def object_open_clinic_tickets_timeframe(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Orders',
            'res_model': 'hospital.clinic.tickets',
            'domain': [('patients_id', '=', self.id)],
            'view_mode': 'calendar,tree,form',
            'target': 'new'
        }


class Insurance(models.Model):
    _name = "hospital.insurance"
    _description = "Patient"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        string="Patient Name",
        required=True,
        tracking=True)
