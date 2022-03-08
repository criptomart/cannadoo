from odoo import fields, models


class PosCreditUpdate(models.Model):
    _inherit = "pos.credit.update"

    # Take first journal with debt field checked as default value
    def _default_journal(self):
        debt_journals = (
            self.env["account.journal"].search([]).filtered(lambda x: x.debt is True)
        )
        if debt_journals:
            return debt_journals[0]

    journal_id = fields.Many2one(
        "account.journal",
        string="Journal",
        required=True,
        domain="[('debt', '=', True)]",
        default=_default_journal,
    )
