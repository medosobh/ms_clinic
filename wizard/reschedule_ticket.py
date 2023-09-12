from datetime import timedelta

from odoo import api, fields, models, _


class RescheduleTicket(models.TransientModel):
    _name = 'hospital.reschedule.ticket'
    _description = 'Reschedule Ticket Wizard'

    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.model
    def default_get(self, fields):
        res = super(RescheduleTicket, self).default_get(fields)
        active_id = self._context.get('clinic_tickets_id')
        if active_id:
            ticket_rec = self.env['hospital.clinic.tickets'].browse(int(active_id))
            res['parent_id'] = ticket_rec.id
            res['patients_id'] = ticket_rec.patients_id
            res['clinics_id'] = ticket_rec.clinics_id
            res['staff_id'] = ticket_rec.staff_id
            res['company_id'] = ticket_rec.company_id
            res['currency_id'] = ticket_rec.currency_id
        return res

    name = fields.Char(
        string="Name",
        index=True,
        required=True,
        tracking=True,
        default=lambda x: _('New'))
    patients_id = fields.Many2one(
        comodel_name="hospital.patients",
        required=True,
        string="Patient")
    # partner_id = fields.Many2one(
    #     comodel_name="res.partner",
    #     related="patients_id.partner_id",
    #     string="Partner")
    clinics_id = fields.Many2one(
        comodel_name="hospital.clinics",
        required=True,
        string="Clinic")
    staff_id = fields.Many2one(
        comodel_name="hospital.staff",
        required=True,
        string="Doctor")
    start_date = fields.Datetime(
        string="Start Date",
        required=True,
        tracking=True)
    end_date = fields.Datetime(
        string="End Date",
        tracking=True,
        store=True,
        compute='_get_end_date')
    parent_id = fields.Many2one(
        comodel_name="hospital.clinic.tickets",
        string='Previous Ticket',
        readonly=True)
    company_id = fields.Many2one(
        string='Company',
        comodel_name='res.company',
        change_default=True,
        default=lambda self: self.env.company,
        required=False,
        tracking=True)
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        related="company_id.currency_id",
        ondelete="set null",
        help="Used to display the currency when tracking monetary values")
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Responsible',
        required=False,
        readonly=True,
        default=lambda self: self.env.user)

    @api.depends('start_date')
    def _get_end_date(self):
        for rec in self:
            if not rec.start_date:
                rec.end_date = rec.start_date
                continue
                # add 20 min to start date
            duration = timedelta(minutes=20, seconds=0)
            rec.end_date = rec.start_date + duration
        return rec.end_date

    def action_create_reschedule_ticket(self):
        self.ensure_one()
        vals = {
            'state': 'draft',
            'patients_id': self.patients_id.id,
            'clinics_id': self.clinics_id.id,
            'staff_id': self.staff_id.id,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'parent_id': self.parent_id.id,
            'company_id': self.company_id.id,
            'currency_id': self.currency_id.id,
            'user_id': self.user_id.id,
        }
        new_rec = self.env['hospital.clinic.tickets'].create(vals)
        # change current ticket state and next date and child ticket
        active_id = self.parent_id.id
        record = self.env['hospital.clinic.tickets'].browse(active_id)
        record.state = 'reschedule'
        record.next_date = new_rec.start_date
        record.child_id = new_rec.id
        # mention assistant to follow the new ticket
        record.activity_schedule(
            'ms_hospital.mail_act_reschedule_ticket',
            user_id=new_rec.staff_id.employee_id.user_id.id,
            note=f'Please check ticket no {new_rec.name}; for patient : '
                 f'{new_rec.patients_id.name} was created.')
        new_rec.activity_schedule(
            'ms_hospital.mail_act_reschedule_ticket',
            user_id=new_rec.staff_id.employee_id.user_id.id,
            note=f'Please check ticket no {new_rec.name}; for patient : '
                 f'{new_rec.patients_id.name} was created.')
