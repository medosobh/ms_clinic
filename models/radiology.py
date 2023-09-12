from odoo import models, fields


class Radiology(models.Model):
    _name = "hospital.radiology"
    _description = "Radiology"
    _check_company_auto = True
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        string="Name", required=True)
    type = fields.Many2one(
        comodel_name="hospital.radiology.type",
        string="Type")
    location = fields.Text(string="Description")
    address = fields.Text(string="Address")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    clinic_tickets_ids = fields.One2many(
        comodel_name="hospital.clinic.tickets",
        inverse_name="clinics_id",
        string="Tickets")
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

    def _compute_tickets_count(self):
        for rec in self:
            tickets_count = self.env['hospital.clinic.tickets'].search_count([
                ('clinics_id', '=', rec.id)
            ])
            rec.tickets_count = tickets_count

    def object_open_tickets_timeframe(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Orders',
            'res_model': 'hospital.clinic.tickets',
            'domain': [('clinics_id', '=', self.id)],
            'view_mode': 'calendar,tree,form',
            'target': 'new'
        }


class RadiologyType(models.Model):
    _name = "hospital.radiology.type"
    _description = "Radiology or Section"
    _check_company_auto = True
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        string="Name",
        required=True)
    active = fields.Boolean(
        string="Active",
        default=True,
        tracking=True)
