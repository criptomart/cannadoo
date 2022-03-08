# Copyright Criptomart <tech@criptomart.net>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Membership Monthly Consumption",
    "summary": "Configure a limit for the monthly consumption of a member. This control is applied for products measured in grams. Show a warning in POS when the limit is reached",
    "version": "12.0.1.0.1",
    "category": "Membership",
    "author": "Criptomart",
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
        "views/res_partner_view.xml",
        "data/ir_cron.xml"
    ],
    "demo": [
    ],
}
