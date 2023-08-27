from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = "product.template"
    _description = "Information about medicines"

    medicine_name = fields.Char(string="Medicine Name", required=True)
    description = fields.Text(string="Description")
    dosage = fields.Float(string="Dosage")
    unit_price = fields.Float(string="Unit Price")
    quantity = fields.Integer(string="Quantity")
    manufacturer = fields.Char(string="Manufacturer")
