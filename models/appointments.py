from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.exceptions import UserError


class Appointments(models.Model):
    _name = "hospital.appointments"
    _description = "Information about appointments"
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
        default="draft", )
    name = fields.Char(
        string="Name", required=True)
    patient_id = fields.Many2one(
        comodel_name="hospital.patients",
        string="Patient")
    clinic_id = fields.Many2one(
        comodel_name="clinic", string="Location")
    doctor_id = fields.Many2one(
        comodel_name="hospital.staff",
        string="Doctor")
    start_date = fields.Datetime(
        string="Start Date", required=True,
        tracking=True, default=datetime.now())
    end_date = fields.Datetime(
        string="End Date", required=True, store=True,
        compute="_get_end_date",
        inverse="_set_end_date", )
    consultation_notes = fields.Text(
        string="Consultation Notes")
    prescription_notes = fields.Text(
        string="Prescription Notes")
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
        comodel_name="res.company", string="Company",
        change_default=True,
        default=lambda self: self.env.company,
        required=False, readonly=True, )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        related="company_id.currency_id",
        readonly=True, ondelete="set null",
        help="Used to display the currency when tracking monetary values")
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
        return rec.customer_invoice_total


class Diagnosis(models.Model):
    _name = "hospital.diagnosis"
    _description = "diagnosis"
    _rec_name = "name"
    _order = "name ASC"

    sequence = fields.Integer(
        string="Sequence", default=10)
    description = fields.Text(
        string="Diagnosis Description", required=True,
        copy=False)
    attachment = fields.Binary(
        string="Attachment File",
        help="Attachment, one file to upload",
        required=False,
        tracking=True, )
    attachment_name = fields.Char(
        string="Attachment Filename", required=False,
        tracking=True)

    def _get_report_base_filename(self):
        return self.attachment_name


class Prescription(models.Model):
    _name = "hospital.prescription"
    _description = "prescription"
    _rec_name = "name"
    _order = "name ASC"

    def _get_report_base_filename(self):
        return self.name

    sequence = fields.Integer(
        string="Sequence", default=10)
    product_id = fields.Many2one(
        comodel_name="product.product", required=True,
        domain="[('categ_id', '=', categ_id)]", )
    name = fields.Text(
        string="Description", required=False)
    categ_id = fields.Many2one(
        related="materials_id.category_id",
        string="Category")
    price_unit = fields.Float(
        string="Price")
    product_uom = fields.Many2one(
        comodel_name="uom.uom",
        string="Unit of Measure",
        related="product_id.uom_id",
        domain="[('category_id', '=', product_uom_category_id)]", )
    qty = fields.Float(
        string="Quantity")
    company_id = fields.Many2one(
        comodel_name="res.company", string="Company",
        related="materials_id.company_id",
        change_default=True,
        default=lambda self: self.env.company,
        required=False,
        readonly=True, )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        related="materials_id.currency_id",
        readonly=True,
        help="Used to display the currency when tracking monetary values", )
    note = fields.Char(
        string="Short Note")
    price_subtotal = fields.Monetary(
        string="Subtotal",
        compute="_compute_subtotal",
        currency_field="currency_id",
        store=True, )
    appointments_id = fields.Many2one(
        comodel_name="hospital.appointments",
        string="Appointment")
