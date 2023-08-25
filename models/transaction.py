from odoo import models, fields, api


class Transaction(models.Model):
    _name = 'ms_clinic.transaction'
    _description = 'Transaction'

    clinic_id = fields.Many2one('clinic', string='Clinic', required=True)
    name = fields.Char(string='Transaction ID', required=True, readonly=True)
    prescription = fields.Text(string='Prescription')

    pharmacist_id = fields.Many2one('ms_clinic.pharmacist', string='Pharmacist', required=True)
    patient_id = fields.Many2one('ms_clinic.patient', string='Patient', required=True)

    trx_date = fields.Datetime(string='Transaction Date', default=fields.Date.today())

    total = fields.Float(string='Total', compute='_compute_total')

    transaction_lines = fields.One2many(
        'ms_clinic.transaction.detail', 
        'transaction_id', 
        string='Transaction Detail'
    )

    @api.depends('transaction_lines.payment_amount')
    def _compute_total(self):
        for record in self:
            record.total = sum(record.transaction_lines.mapped('payment_amount'))

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('transaction_increment') or 'New'
        return super(Transaction, self).create(vals)       


class TransactionDetail(models.Model):
    _name = 'ms_clinic.transaction.detail'
    _description = 'Transaction Detail'

    transaction_id = fields.Many2one('ms_clinic.transaction', string='Transaction')
    medicine_id = fields.Many2one('ms_clinic.medicine', string='Medicine')
    payment_amount = fields.Float(string='Payment Amount')
