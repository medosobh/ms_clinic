from datetime import datetime

from odoo import models, fields


class Tickets(models.Model):
    _name = "hospital.tickets"
    _description = "Information about tickets"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("confirm", "Confirm"),
            ("inspection", "Inspection"),
            ("reschedule", "Reschedule"),
            ("closed", "Closed"),
        ],
        string="State",
        default="draft")
    name = fields.Char(
        string="Name",
        required=True)
    patients_id = fields.Many2one(
        comodel_name="hospital.patients",
        string="Patient")
    clinics_id = fields.Many2one(
        comodel_name="hospital.clinics",
        string="Location")
    staff_id = fields.Many2one(
        comodel_name="hospital.staff",
        string="Doctor")
    start_date = fields.Datetime(
        string="Start Date", required=True,
        tracking=True, default=datetime.now())
    end_date = fields.Datetime(
        string="End Date",
        required=True, store=True,
        compute="_get_end_date",
        inverse="_set_end_date", )
    consultation_notes = fields.Text(
        string="Consultation Notes")
    prescription_notes = fields.Text(
        string="Prescription Notes")
    medicine_line_ids = fields.One2many(
        comodel_name='hospital.medicine.line',
        inverse_name='tickets_id',
        string="Medicine lines")
    diagnosis_ids = fields.One2many(
        comodel_name='hospital.diagnosis',
        inverse_name='tickets_id',
        string="Diagnosis lines")
    prescriptions_ids = fields.One2many(
        comodel_name='hospital.prescriptions',
        inverse_name='tickets_id',
        string="Prescriptions lines")
    billing_amount = fields.Float(
        string="Billing Amount")
    payment_amount = fields.Float(
        string="Payment Amount")
    payment_date = fields.Date(
        string="Payment Date")
    analytic_account_id = fields.Reference(
        selection=[("account.analytic.account", "Analytic Account")],
        string="Analytic Account", )
    next_date = fields.Date(
        string="Appointment Date",
        default=fields.Date.today())
    parent_id = fields.Many2one(
        comodel_name="account.group", index=True,
        ondelete="cascade", readonly=True)
    parent_path = fields.Char(
        index=True)
    child_id = fields.One2many(
        comodel_name="farm.locations",
        inverse_name="parent_id",
        string="Child location")
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        change_default=True,
        default=lambda self: self.env.company,
        required=False,
        readonly=True)
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        related="company_id.currency_id",
        readonly=True, ondelete="set null",
        help="Used to display the currency when tracking monetary values")
    sales_id = fields.Many2one(
        comodel_name='hospital.sales',
        string="Sales Orders")
    sales_ids = fields.One2many(
        comodel_name='hospital.sales',
        inverse_name='tickets_id',
        string="Sales Orders")
    customer_invoice_count = fields.Integer(
        string="Patient Invoice Count",
        compute="_compute_customer_invoice_count")
    customer_invoice_total = fields.Integer(
        string="Patient Invoice Total",
        compute="_compute_customer_invoice_total")

    def set_to_draft(self):
        self.state = 'draft'

    def set_to_confirm(self):
        self.state = 'confirm'

    def set_to_inspection(self):
        self.state = 'inspection'

    def set_to_reschedule(self):
        self.state = 'reschedule'

    def set_to_closed(self):
        self.state = 'closed'

    def _compute_customer_invoice_count(self):
        for rec in self:
            customer_invoice_count = self.env["account.move"].search_count(
                [("invoice_origin", "=", rec.name)])
            rec.customer_invoice_count = customer_invoice_count

    def _compute_customer_invoice_total(self):
        for rec in self:
            total_debit = sum(self.env["account.move.line"].search(
                [("sales_id", "=", rec.id)]).mapped("debit"))
            total_credit = sum(self.env["account.move.line"].search(
                [("sales_id", "=", rec.id)]).mapped("credit"))
            rec.customer_invoice_total = total_debit + total_credit

    def action_customer_invoice(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Customer Invoices',
            'res_model': 'account.move',
            'domain': [('invoice_origin', '=', self.name)],
            'view_mode': 'tree',
            'context': {},
            'target': 'new'
        }


class Diagnosis(models.Model):
    _name = "hospital.diagnosis"
    _description = "diagnosis"
    _order = "diagnosis_date ASC"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    sequence = fields.Integer(
        string="Sequence",
        default=10)
    diagnosis_date = fields.Text(
        string="Date",
        required=False,
        tracking=True)
    note = fields.Char(
        string="Short Note",
        tracking=True)
    attachment = fields.Binary(
        string="Attachment File",
        help="Attachment, one file to upload",
        required=False,
        tracking=True)
    attachment_name = fields.Char(
        string="Attachment Filename",
        required=False,
        tracking=True)
    tickets_id = fields.Many2one(
        comodel_name="hospital.tickets",
        string="Appointment")

    def _get_report_base_filename(self):
        return self.attachment_name


class Prescriptions(models.Model):
    _name = "hospital.prescriptions"
    _description = "Prescription"
    _order = "prescription_date ASC"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    sequence = fields.Integer(
        string="Sequence",
        default=10)
    prescription_date = fields.Text(
        string="Date",
        required=False)
    note = fields.Char(
        string="Short Note",
        tracking=True)
    attachment = fields.Binary(
        string="Attachment File",
        help="Attachment, one file to upload",
        required=False,
        tracking=True)
    attachment_name = fields.Char(
        string="Attachment Filename",
        required=False,
        tracking=True)
    tickets_id = fields.Many2one(
        comodel_name="hospital.tickets",
        string="Appointment")

    def _get_report_base_filename(self):
        return self.attachment_name


class MedicineLine(models.Model):
    _name = 'hospital.medicine.line'
    _description = 'Medicine Line'

    name = fields.Text(
        string='Description',
        required=True)
    sequence = fields.Integer(
        string='Sequence',
        default=10)
    product_id = fields.Many2one(
        comodel_name='product.product',
        required=True)
    price_unit = fields.Float(
        string='Price')
    product_uom = fields.Many2one(
        comodel_name='uom.uom',
        string='Unit of Measure',
        related='product_id.uom_id')
    qty = fields.Float(
        string='Quantity')
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        related='sales_id.company_id',
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
    note = fields.Char(
        string='Short Note')
    price_subtotal = fields.Monetary(
        string='Subtotal',
        compute='_compute_subtotal',
        currency_field='currency_id',
        store=True)
    tickets_id = fields.Many2one(
        comodel_name='hospital.tickets',
        string='Appointment ticket')
