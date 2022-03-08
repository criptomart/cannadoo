# Copyright 2016 Antonio Espinosa <antonio.espinosa@tecnativa.com>
# Copyright 2017 David Vidal <david.vidal@tecnativa.com>
# Copyright 2017 Luis M. Ontalba <luis.martinez@tecnativa.com>
# Copyright 2017-2018 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Membership ID Pictures",
    "summary": "Add 2 fields to store images of the ID card",
    "version": "12.0.1.0.1",
    "category": "Membership",
    "author": "Criptomart, "
              "Odoo Community Association (OCA)",
    "website": "https://github.com/oca/vertical-association",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "membership",
    ],
    "data": [
        "views/res_partner_view.xml",
    ],
    "demo": [
    ],
}
