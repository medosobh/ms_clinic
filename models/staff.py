from datetime import date

from odoo import models, fields, api


class Staff(models.Model):
    _name = "hospital.staff"
    _description = "Staff"
    _check_company_auto = True
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
    employee_id = fields.Many2one(
        comodel_name="hr.employee",
        required=True,
        string="Employee")
    job_title = fields.Char(
        related="employee_id.job_title",
        string="Job Title")
    user_id = fields.Many2one(
        comodel_name='res.users', string='Doctor Internal User',
        required=True,
        readonly=True,
        tracking=True,
        default=lambda self: self.employee_id.user_id)
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
    specialization = fields.Char(
        string="Specialization")
    tickets_ids = fields.One2many(
        comodel_name="hospital.clinic.tickets",
        inverse_name="staff_id",
        string="Tickets")
    tickets_count = fields.Integer(
        string="Operation Count",
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

    def _compute_tickets_count(self):
        for rec in self:
            tickets_count = self.env['hospital.clinic.tickets'].search_count([
                ('staff_id', '=', rec.id)
            ])
            rec.tickets_count = tickets_count

    def object_open_tickets_timeframe(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Orders',
            'res_model': 'hospital.clinic.tickets',
            'domain': [('staff_id', '=', self.id)],
            'view_mode': 'calendar,tree,form',
            'target': 'new'
        }
