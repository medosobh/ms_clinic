from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime, timedelta

class Transaction(models.Model):
    _name = "ms_hospital.transaction"
    _description = "Transaction"

    name = fields.Char(string="Transaction ID", required=True, readonly=True)
    clinic_id = fields.Many2one("ms_hospital.clinic", string="Clinic", required=True)
    prescription = fields.Text(string="Prescription")
    pharmacist_id = fields.Many2one(
        "ms_hospital.pharmacist", string="Pharmacist", required=True
    )
    patient_id = fields.Many2one("ms_hospital.patient", string="Patient", required=True)
    trx_date = fields.Datetime(string="Transaction Date", default=fields.Date.today())
    total = fields.Float(string="Total", compute="_compute_total")
    transaction_lines = fields.One2many(
        "ms_hospital.transaction.detail", "transaction_id", string="Transaction Detail"
    )

    @api.depends("transaction_lines.payment_amount")
    def _compute_total(self):
        for record in self:
            record.total = sum(record.transaction_lines.mapped("payment_amount"))

    @api.model
    def create(self, vals):
        vals["name"] = (
            self.env["ir.sequence"].next_by_code("transaction_increment") or "New"
        )
        return super(Transaction, self).create(vals)


class TransactionDetail(models.Model):
    _name = "ms_hospital.transaction.detail"
    _description = "Transaction Detail"

    transaction_id = fields.Many2one("ms_hospital.transaction", string="Transaction")
    medicine_id = fields.Many2one("ms_hospital.medicine", string="Medicine")
    payment_amount = fields.Float(string="Payment Amount")
