from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"
    _description = "Information about medicines"

    medicine_name = fields.Char(
        string="Medicine Name")
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
