# Copyright 2021 CriptMart <tech@criptomart.net>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Membership Cannadoo",
    "summary": "Modificaciones al módulo membership para cannadoo.",
    "version": "12.0.1.0.0",
    "category": "Membership",
    "author": "Criptomart ",
    "website": "https://criptomart.net",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "membership",
        "membership_extension",
        "membership_variable_period",
        "base_user_role",
        "pos_access_right",
        "pos_debt_notebook",
        "partner_contact_birthdate",
        "membership_guarantor",
        "membership_pos_info",
        "membership_id_pics",
        "membership_monthly_consumption",
    ],
    "qweb": [],
    "data": [
        "data/roles.xml",
        "views/res_partner_view.xml",
        "views/membership_category_view.xml",
        "views/templates.xml",
        "views/product_template_view.xml",
    ],
}
