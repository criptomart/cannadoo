from odoo import SUPERUSER_ID, _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class PosSession(models.Model):
    _inherit = "pos.session"

    put_take_money_sum = fields.Float(
        string="Suma de movimientos de caja",
        help="Campo computado que almacena la suma de los movimientos de caja que se realizan con las opciones de poner y sacar dinero.",
        readonly=True,
        default=0.0,
        compute="_compute_put_take_money_sum",
    )

    pos_transaction_sum = fields.Float(
        string="Suma de transacciones de dispensario",
        help="Campo computado que almacena la suma de movimientos de efectivo en dispensario.",
        readonly=True,
        default=0.0,
        compute="_compute_put_take_money_sum",
    )

    def _compute_put_take_money_sum(self):
        for session in self:
            put_take_money_sum = 0
            pos_transaction_sum = 0
            for statement in session.statement_ids:
                if (
                    statement.journal_id.type == "cash"
                    and not statement.journal_id.debt
                ):
                    for line in statement.line_ids:
                        if not line.partner_id:
                            put_take_money_sum += line.amount
                        else:
                            pos_transaction_sum += line.amount
            session.put_take_money_sum = put_take_money_sum
            session.pos_transaction_sum = pos_transaction_sum

    @api.model
    def create(self, values):
        config_id = values.get("config_id") or self.env.context.get("default_config_id")
        if not config_id:
            raise UserError(_("You should assign a Point of Sale to your session."))

        # journal_id is not required on the pos_config because it does not
        # exists at the installation. If nothing is configured at the
        # installation we do the minimal configuration. Impossible to do in
        # the .xml files as the CoA is not yet installed.
        pos_config = self.env["pos.config"].browse(config_id)
        ctx = dict(self.env.context, company_id=pos_config.company_id.id)
        if not pos_config.journal_id:
            default_journals = pos_config.with_context(ctx).default_get(
                ["journal_id", "invoice_journal_id"]
            )
            if not default_journals.get("journal_id") or not default_journals.get(
                "invoice_journal_id"
            ):
                raise UserError(
                    _(
                        "Unable to open the session. You have to assign a sales journal to your point of sale."
                    )
                )
            pos_config.with_context(ctx).sudo().write(
                {
                    "journal_id": default_journals["journal_id"],
                    "invoice_journal_id": default_journals["invoice_journal_id"],
                }
            )
        # define some cash journal if no payment method exists
        if not pos_config.journal_ids:
            Journal = self.env["account.journal"]
            journals = Journal.with_context(ctx).search(
                [("journal_user", "=", True), ("type", "=", "cash")]
            )
            if not journals:
                journals = Journal.with_context(ctx).search([("type", "=", "cash")])
                if not journals:
                    journals = Journal.with_context(ctx).search(
                        [("journal_user", "=", True)]
                    )
            if not journals:
                raise ValidationError(
                    _(
                        "No payment method configured! \nEither no Chart of Account is installed or no payment method is configured for this POS."
                    )
                )
            journals.sudo().write({"journal_user": True})
            pos_config.sudo().write({"journal_ids": [(6, 0, journals.ids)]})

        # se está duplicando el nombre de la sesión.
        pos_name = ""
        #        pos_name = self.env['ir.sequence'].with_context(ctx).next_by_code('pos.session')
        #        if values.get('name'):
        #            pos_name += ' ' + values['name']

        statements = []
        ABS = self.env["account.bank.statement"]
        uid = (
            SUPERUSER_ID
            if self.env.user.has_group("point_of_sale.group_pos_user")
            else self.env.user.id
        )
        for journal in pos_config.journal_ids:
            # set the journal_id which should be used by
            # account.bank.statement to set the opening balance of the
            # newly created bank statement
            # Aquí sobreescribimos el método para arrancar las cajas a cero.
            ctx["journal_id"] = (
                journal.id
                if pos_config.cash_control and journal.type == "cash"
                else False
            )
            st_values = {
                "journal_id": journal.id,
                "user_id": self.env.user.id,
                "name": pos_name,
                "balance_start": 0,
            }

            statements.append(ABS.with_context(ctx).sudo(uid).create(st_values).id)

        values.update(
            {
                "name": pos_name,
                "statement_ids": [(6, 0, statements)],
                "config_id": config_id,
            }
        )

        res = super(PosSession, self.with_context(ctx).sudo(uid)).create(values)
        if not pos_config.cash_control:
            res.action_pos_session_open()

        return res
