from odoo import models, fields, api


class Services(models.Model):
    _name = 'hospital.services'
    _description = 'Service'
    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(
        string='Name',
        required=True,
        copy=False)
    description = fields.Text(
        string="Description")
    product_id = fields.Many2one(
        comodel_name='product.product')
    unit_price = fields.Float(
        string=' Unit Price',
        required=True)
    product_uom = fields.Many2one(
        comodel_name='uom.uom',
        # related='product_id.uom_id'
        string='Unit of Measure',
        required=False)
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        change_default=True,
        default=lambda self: self.env.company,
        required=True,
        readonly=True)
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        related='company_id.currency_id',
        readonly=True,
        help="Used to display the currency when tracking monetary values")
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Responsible',
        required=False,
        readonly=True,
        default=lambda self: self.env.user)

    @api.model
    def create(self, vals):
        # self.ensure_one()
        product_vals = {
            'name': vals['name'],
            'sale_ok': True,
            'purchase_ok': False,
            'detailed_type': 'service',
            'invoice_policy': 'delivery',
            'list_price': vals['unit_price'],
            'description': vals['description'],
            'description_sale': vals['description'],
            'taxes_id': None,
            # 'company_id': vals['company_id'],
        }
        invoice = self.env['product.product'].create(product_vals)
        vals.update({
            'product_id': invoice.id,
        })
        return super(Services, self).create(vals)

