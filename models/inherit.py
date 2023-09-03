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


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    # expense already maintained in he.expense model
    sales_id = fields.Many2one(
        comodel_name='hospital.sales',
        string="Hospital Sales")
    move_type = fields.Selection(
        related="move_id.move_type")

