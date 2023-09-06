from datetime import timedelta, datetime

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class Tickets(models.Model):
    _name = "hospital.tickets"
    _description = "Ticket"
    _check_company_auto = True
    _inherit = ["mail.thread", "mail.activity.mixin"]

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("confirm", "Confirm"),
            ("inspection", "Inspection"),
            ("reschedule", "Reschedule"),
            ("invoicing", "Invoicing"),
            ("closed", "Closed"),
        ],
        string="State",
        group_expand='_group_expand_states',
        default="draft")
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
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        related="patients_id.partner_id",
        string="Partner")
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
    invoice_amount = fields.Monetary(
        string="Invoice Amount",
        compute="_compute_invoice_amount",
        currency_field='currency_id')
    payment_amount = fields.Monetary(
        string="Payment Amount",
        compute="_compute_payment_amount",
        currency_field='currency_id')
    payment_date = fields.Date(
        string="Payment Date",
        compute="_compute_payment_date")
    next_date = fields.Datetime(
        string="Reschedule Date",
        readonly=True,
        tracking=True)
    parent_id = fields.Many2one(
        comodel_name="hospital.tickets",
        string='Previous Ticket',
        readonly=True)
    child_id = fields.Many2one(
        comodel_name="hospital.tickets",
        string="Next Ticket",
        readonly=True)
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        index=True,
        required=True,
        default=lambda self: self.env.company)
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
    consultation_notes = fields.Text(
        string="Consultation Notes")
    prescription_notes = fields.Text(
        string="Prescription Notes")
    diagnose_id = fields.Many2one(
        comodel_name='hospital.diagnose.line',
        string="diagnose lines")
    diagnose_ids = fields.One2many(
        comodel_name='hospital.diagnose.line',
        inverse_name='tickets_id',
        string="Diagnosis")
    prescription_line_id = fields.Many2one(
        comodel_name='hospital.prescription.line',
        string="prescription lines")
    prescription_line_ids = fields.One2many(
        comodel_name='hospital.prescription.line',
        inverse_name='tickets_id',
        string="Prescriptions")
    invoice_line_ids = fields.One2many(
        comodel_name='hospital.ticket.invoice.line',
        inverse_name='tickets_id',
        string="Invoice Lines")
    customer_invoice_count = fields.Integer(
        string="Patient Invoice Count",
    )
    customer_invoice_total = fields.Integer(
        string="Patient Invoice Total",
    )
    active = fields.Boolean(
        string="Active",
        default=True,
        tracking=True)

    @api.model
    def create(self, vals):
        if not vals.get('name') or vals['name'] == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'ms_hospital.tickets') or _('New')
        return super(Tickets, self).create(vals)

    @api.constrains('parent_id')
    def _check_category_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_('You cannot create recursive tickets.'))

    #

    @api.constrains('child_id')
    def _check_category_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_('You cannot create recursive tickets.'))

    def _group_expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]

    def set_to_draft(self):
        self.state = 'draft'

    def set_to_confirm(self):
        self.state = 'confirm'

    def set_to_inspection(self):
        self.state = 'inspection'

    def set_to_invoicing(self):
        self.state = 'invoicing'
        # create Customer Invoice in background and open form view.
        self.ensure_one()
        move_type = self._context.get('default_move_type', 'out_invoice')
        journal = self.env['account.move'].with_context(
            default_move_type=move_type)._get_default_journal()
        if not journal:
            raise UserError(
                _('Please define an accounting sales journal for the company %s (%s).',
                  self.company_id.name,
                  self.company_id.id))
        partner_invoice_id = self.partner_id.address_get(['invoice'])[
            'invoice']
        partner_bank_id = self.partner_id.commercial_partner_id.bank_ids.filtered_domain(
            ['|', ('company_id', '=', False),
             ('company_id', '=', self.company_id.id)])[:1]
        invoice_vals = {
            'state': 'draft',
            'ref': self.name or '',
            'invoice_date': self.start_date,
            'move_type': move_type,
            # 'narration': self.notes,
            'currency_id': self.currency_id.id,
            'invoice_user_id': self.user_id and self.user_id.id or self.env.user.id,
            'partner_id': partner_invoice_id,
            # 'fiscal_position_id': (self.fiscal_position_id or
            # self.fiscal_position_id.get_fiscal_position(
            # partner_invoice_id)).id,
            'payment_reference': self.name or '',
            'partner_bank_id': partner_bank_id.id,
            'journal_id': journal.id,  # company comes from the journal
            'invoice_origin': self.name,
            # 'invoice_payment_term_id': self.payment_term_id.id,
            'invoice_line_ids': [(0, 0, {
                'sequence': self.invoice_line_ids.sequence,
                'product_id': self.invoice_line_ids.product_id.id,
                'product_uom_id': self.invoice_line_ids.product_uom.id,
                'quantity': self.invoice_line_ids.qty,
                'price_unit': self.invoice_line_ids.price_unit,
                # 'analytic_account_id': self.analytic_account_id.id,
                # 'sales_id': self.id,
            })],
            'company_id': self.company_id.id,
        }
        invoice = self.env['account.move'].create(invoice_vals)
        result = self.env['ir.actions.act_window']._for_xml_id(
            'account.action_move_out_invoice_type'
        )
        res = self.env.ref('account.view_move_form', False)
        form_view = [(res and res.id or False, 'form')]
        result['views'] = form_view + [(state, view) for state, view in
                                       result['views'] if view != 'form']
        result['res_id'] = invoice.id
        return result

    def _compute_invoice_amount(self):
        for rec in self:
            customer_invoice_total = sum(
                self.env['account.move'].search([
                    ('ref', '=', rec.name),
                    ('move_type', '=', 'out_invoice')
                ]).mapped('amount_total')
            )

            rec.invoice_amount = customer_invoice_total
        return rec.invoice_amount

    def _compute_payment_amount(self):
        for rec in self:
            customer_payment_total = sum(
                self.env['account.move'].search([
                    ('ref', '=', rec.name),
                    ('move_type', '=', 'entry')
                ]).mapped('amount_total')
            )

            rec.payment_amount = customer_payment_total
        return rec.payment_amount

    def _compute_payment_date(self):
        for rec in self:
            payment_date = self.env['account.move'].search([
                ('ref', '=', rec.name),
                ('move_type', '=', 'entry')
            ], limit=1)

            rec.payment_date = payment_date.date
        return rec.payment_date

    def collect_money(self):
        # account.payment
        # account.action_account_payments
        # pass context partner, amount and memo
        return {
            'type': 'ir.actions.act_window',
            'name': 'Collect Invoice',
            'res_model': 'account.payment',
            'view_mode': 'form',
            'context': {
                'default_payment_type': 'inbound',
                'default_partner_id': self.partner_id.id,
                'default_amount': self.invoice_amount,
                'default_ref': self.name,
            },
            'target': 'new'
        }

    def set_to_reschedule(self):
        self.state = 'reschedule'

    def set_to_closed(self):
        self.state = 'closed'

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

    def action_customer_invoice(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Customer Invoices',
            'res_model': 'account.move',
            'domain': [
                ('ref', '=', self.name),
                ('move_type', '=', 'out_invoice')
            ],
            'view_mode': 'tree',
            'context': {},
            'target': 'new'
        }

    def action_customer_payment(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Customer Payment',
            'res_model': 'account.move',
            'domain': [
                ('ref', '=', self.name),
                ('move_type', '=', 'entry')
            ],
            'view_mode': 'tree',
            'context': {},
            'target': 'new'
        }


class DiagnoseLine(models.Model):
    _name = "hospital.diagnose.line"
    _description = "diagnosis"
    _order = "diagnosis_date ASC"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _get_report_base_filename(self):
        return self.attachment_name

    sequence = fields.Integer(
        string="Sequence",
        default=10)
    diagnosis_date = fields.Date(
        string="Date",
        required=False,
        tracking=True,
        default=datetime.today())
    note = fields.Text(
        string="Note",
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
        string="Ticket")
    patients_id = fields.Many2one(
        comodel_name="hospital.patients",
        string="Patient")
    user_id = fields.Many2one(
        comodel_name='res.users', string='Responsible',
        required=False,
        readonly=True,
        tracking=True,
        default=lambda self: self.env.user)


class PrescriptionLine(models.Model):
    _name = "hospital.prescription.line"
    _description = "Prescription"
    _order = "sequence ASC"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    sequence = fields.Integer(
        string="Sequence",
        default=10)
    product_id = fields.Many2one(
        comodel_name='product.product',
        required=True,
        string="medicine")
    note = fields.Char(
        string="Note",
        tracking=True)
    tickets_id = fields.Many2one(
        comodel_name="hospital.tickets",
        string="Ticket")
    patients_id = fields.Many2one(
        comodel_name="hospital.patients",
        string="Patient")
    user_id = fields.Many2one(
        comodel_name='res.users', string='Responsible',
        required=False,
        readonly=True,
        tracking=True,
        default=lambda self: self.env.user)


class TicketInvoiceLine(models.Model):
    _name = 'hospital.ticket.invoice.line'
    _description = 'Ticket Invoice Line'

    name = fields.Text(
        string='Description',
        required=True)
    sequence = fields.Integer(
        string='Sequence',
        default=10)
    services_id = fields.Many2one(
        comodel_name='hospital.services',
        string='Service')
    product_id = fields.Many2one(
        comodel_name='product.product',
        related='services_id.product_id',
        string='Product')
    price_unit = fields.Float(
        related='product_id.list_price',
        string='Price')
    product_uom = fields.Many2one(
        comodel_name='uom.uom',
        related='product_id.uom_id',
        string='Unit of Measure')
    qty = fields.Float(
        default=1,
        required=True,
        string='Quantity')
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        related='tickets_id.company_id',
        change_default=True,
        required=False,
        readonly=True)
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        related='tickets_id.currency_id',
        readonly=True,
        help="Used to display the currency when tracking monetary values")
    price_subtotal = fields.Monetary(
        string='Subtotal',
        compute='_compute_subtotal',
        currency_field='currency_id',
        store=True)
    tickets_id = fields.Many2one(
        comodel_name='hospital.tickets',
        string='Ticket')

    @api.onchange('product_id')
    def onchange_price_unit(self):
        if not self.product_id:
            self.price_unit = 0
            return
        self.price_unit = self.product_id.list_price

    @api.depends('price_unit', 'qty')
    def _compute_subtotal(self):
        for rec in self:
            rec.price_subtotal = rec.price_unit * rec.qty
