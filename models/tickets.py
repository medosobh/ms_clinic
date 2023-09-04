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
        string="Patient")
    # partner_id = fields.Many2one(
    #     comodel_name="res.partner",
    #     related="patients_id.partner_id",
    #     string="Partner")
    clinics_id = fields.Many2one(
        comodel_name="hospital.clinics",
        string="Clinic")
    staff_id = fields.Many2one(
        comodel_name="hospital.staff",
        string="Doctor")
    # employee_id = fields.Many2one(
    #     comodel_name="hr.employee",
    #     related="staff_id.partner_id",
    #     string="Employee at HR")
    start_date = fields.Datetime(
        string="Start Date",
        tracking=True)
    end_date = fields.Datetime(
        string="End Date",
        tracking=True,
        store=True,
        compute='_get_end_date')
    billing_amount = fields.Monetary(
        string="Billing Amount",
        currency_field='currency_id')
    payment_amount = fields.Monetary(
        string="Payment Amount",
        currency_field='currency_id')
    payment_date = fields.Date(
        string="Payment Date")
    next_date = fields.Datetime(
        string="Reschedule Date",
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
    # sales_line_ids = fields.One2many(
    #     comodel_name='hospital.ticket.sales.line',
    #     inverse_name='tickets_id',
    #     string="Sales Orders")
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

    def _compute_customer_invoice_count(self):
        self.ensure_one()
        # for rec in self:
        #     customer_invoice_count = self.env["account.move"].search_count(
        #         [("invoice_origin", "=", rec.name)])
        #     rec.customer_invoice_count = customer_invoice_count
        return

    def _compute_customer_invoice_total(self):
        self.ensure_one()
        # for rec in self:
        #     total_debit = sum(self.env["account.move.line"].search(
        #         [("tickets_id", "=", rec.id)]).mapped("debit"))
        #     total_credit = sum(self.env["account.move.line"].search(
        #         [("tickets_id", "=", rec.id)]).mapped("credit"))
        #     rec.customer_invoice_total = total_debit + total_credit
        return

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

    def button_hospital_customer_invoice(self):
        # create Customer Invoice in background and open form view.
        self.ensure_one()
        # check analytic_account_id created

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
                'sequence': self.sales_line_ids.sequence,
                'product_id': self.sales_line_ids.product_id.id,
                'product_uom_id': self.sales_line_ids.product_uom.id,
                'quantity': self.sales_line_ids.qty,
                'price_unit': self.sales_line_ids.price_unit,
                # 'analytic_account_id': self.analytic_account_id.id,
                # 'sales_id': self.id,
            })],
            'company_id': self.company_id.id,
        }
        invoice = self.env['account.move'].create(invoice_vals)
        result = self.env['ir.actions.act_window']._for_xml_id(
            'account.action_move_out_invoice_type')
        res = self.env.ref('account.view_move_form', False)
        form_view = [(res and res.id or False, 'form')]
        result['views'] = form_view + \
                          [(state, view)
                           for state, view in result['views'] if
                           view != 'form']
        result['res_id'] = invoice.id
        return result


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
        required=True)
    note = fields.Char(
        string="",
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


class TicketSalesLine(models.Model):
    _name = 'hospital.ticket.sales.line'
    _description = 'Ticket Sales Line'

    name = fields.Text(
        string='Description',
        required=True)
    sequence = fields.Integer(
        string='Sequence',
        default=10)
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product')
    price_unit = fields.Float(
        string='Price')
    product_uom = fields.Many2one(
        comodel_name='uom.uom',
        string='Unit of Measure',
        related='product_id.uom_id',
        domain="[('category_id', '=', product_uom_category_id)]")
    qty = fields.Float(
        string='Quantity')
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        related='tickets_id.company_id',
        change_default=True,
        default=lambda self: self.env.company,
        required=False,
        readonly=True)
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        related='tickets_id.currency_id',
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
