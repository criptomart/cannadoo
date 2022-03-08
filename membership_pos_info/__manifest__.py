# Copyright 2021 CriptoMart <tech@criptomart.net>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Membership POS Info",
    "summary": "Show status, category and date affiliation in PoS. Process PoS membership orders lines.",
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
        "point_of_sale"
    ],
    "qweb": [
        "static/src/xml/point_of_sale.xml",
    ],
    "data": [
        "views/assets.xml",
   ],
}
