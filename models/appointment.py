from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime, timedelta


class Appointment(models.Model):
    _name = "ms_hospital.appointment"
    _description = "Information about appointments"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", required=True)
    clinic_id = fields.Many2one("clinic", string="Location")
    patient_id = fields.Many2one("ms_hospital.patient", string="Patient")
    doctor_id = fields.Many2one("ms_hospital.doctor", string="Doctor")
    appointment_date = fields.Date(
        string="Appointment Date", default=fields.Date.today()
    )
    start_date = fields.Datetime(
        string="Start Date", required=True, tracking=True, default=datetime.now()
    )
    end_date = fields.Datetime(
        string="End Date",
        required=True,
        store=True,
        compute="_get_end_date",
        inverse="_set_end_date",
    )
    consultation_notes = fields.Text(string="Consultation Notes")
    prescription_notes = fields.Text(string="Prescription Notes")
    billing_amount = fields.Float(string="Billing Amount")
    payment_amount = fields.Float(string="Payment Amount")
    payment_date = fields.Date(string="Payment Date")
    analytic_account_id = fields.Reference(
        selection=[
            ('account.analytic.account', 'Analytic Account')
        ],
        string='Analytic Account')

    @api.depends("start_date")
    def _get_end_date(self):
        for r in self:
            if not (r.start_date and r.p_days):
                r.end_date = r.start_date
                continue
            # Add duration to start_date, but: Monday + 5 days = Saturday, so
            # subtract one second to get on Friday instead
            p_days = timedelta(days=r.p_days, seconds=0)
            r.end_date = r.start_date + p_days
        return r.end_date

    def _set_end_date(self):
        for r in self:
            if not (r.start_date and r.end_date):
                raise UserError(
                    (
                        "Please define start and End date for current project for the company %s (%s)."
                    )
                    % (self.company_id.name, self.company_id.id)
                )
                continue

            # Compute the difference between dates, but: Friday - Monday = 4 days,
            # so add one day to get 5 days instead
            r.p_days = (r.end_date - r.start_date).days
        return r.p_days

    @api.onchange("patient_id")
    def onchange_patient_id(self):
        if self.patient_id:
            today = datetime.now().strftime("%Y%m%d")
            self.name = "APPOINTMENT/" + self.patient_id.name + "/" + today

    def open_create_appointment_form(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Create Appointment",
            "res_model": "ms_hospital.appointment",
            "view_mode": "form",
            "target": "current",
            "context": {
                "default_patient_id": self.patient_id.id,
                "default_clinic_id": self.clinic_id.id,
            },
        }

    def open_schedule_appointment_form(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Schedule Appointment",
            "res_model": "ms_hospital.appointment",
            "view_mode": "form",
            "target": "current",
            "context": {
                "default_patient_id": self.patient_id.id,
                "default_clinic_id": self.clinic_id.id,
            },
        }

    def open_appointment_calendar(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Appointment Calendar",
            "res_model": "ms_hospital.appointment",
            "view_mode": "calendar,tree",
            "target": "current",
        }

    def open_billing(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Billing",
            "res_model": "ms_hospital.appointment",
            "view_mode": "form",
            "target": "current",
        }

    def open_payment(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Payment",
            "res_model": "ms_hospital.appointment",
            "view_mode": "form",
            "target": "current",
        }


class diagnosis(models.Model):
    _name = 'diagnosis'
    _description = 'diagnosis'
    _rec_name = 'name'
    _order = 'name ASC'

    def _get_report_base_filename(self):
        return self.name

    sequence = fields.Integer(
        string='Sequence',
        default=10)
    description = fields.Text(
        string='Diagnosis Description',
        required=True,
        copy=False
    )
    attachment = fields.Binary(
        string="Attachment File",
        help='Attachment, one file to upload',
        required=False,
        tracking=True,
    )
    attachment_name = fields.Char(
        string='Attachment Filename',
        required=False,
        tracking=True
    )


class prescription(models.Model):
    _name = 'prescription'
    _description = 'prescription'
    _rec_name = 'name'
    _order = 'name ASC'

    def _get_report_base_filename(self):
        return self.name

    sequence = fields.Integer(
        string='Sequence',
        default=10)
    product_id = fields.Many2one(
        comodel_name='product.product',
        required=True,
        domain="[('categ_id', '=', categ_id)]")
    name = fields.Text(
        string='Description',
        required=False)
    categ_id = fields.Many2one(
        related='materials_id.category_id',
        string='Category')
    price_unit = fields.Float(
        string='Price')
    product_uom = fields.Many2one(
        comodel_name='uom.uom',
        string='Unit of Measure',
        related='product_id.uom_id',
        domain="[('category_id', '=', product_uom_category_id)]")
    qty = fields.Float(
        'Quantity')
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        related='materials_id.company_id',
        change_default=True,
        default=lambda self: self.env.company,
        required=False,
        readonly=True)
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        related='materials_id.currency_id',
        readonly=True,
        help="Used to display the currency when tracking monetary values")
    note = fields.Char(
        string='Short Note')
    price_subtotal = fields.Monetary(
        string='Subtotal',
        compute='_compute_subtotal',
        currency_field='currency_id',
        store=True)
    appointments_id = fields.Many2one(
        comodel_name='ms_hospital.appointments',
        string='Appointment')
