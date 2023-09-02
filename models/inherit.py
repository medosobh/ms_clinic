from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"
    _description = "Information about medicines"

    medicine_name = fields.Char(
        string="Medicine Name",
        required=True)
    medicine_description = fields.Text(
        string="Medicine Description")
    dosage = fields.Float(
        string="Dosage")
    medicine_unit_price = fields.Float(
        string="Unit Price")
    quantity = fields.Integer(
        string="Quantity")
    manufacturer = fields.Char(
        string="Manufacturer")
    service_name = fields.Char(
        string="Service Name",
        required=True)
    service_description = fields.Text(
        string="Service Description")
    service_unit_price = fields.Float(string="Unit Price")


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    clinics_reference = fields.Reference(
        selection=[
            ('hospital.clinics', 'Clinic')
        ],
        string='Clinic')
