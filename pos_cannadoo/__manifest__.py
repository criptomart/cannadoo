# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Point of Sale - Cannadoo",
    "version": "12.0.1.0.0",
    "category": "Point of Sale",
    "summary": "Point of Sale - Cannadoo modifications",
    "author": "Criptomart",
    "website": "https://criptomart.net",
    "license": "AGPL-3",
    "depends": ["point_of_sale", "pos_debt_notebook", "pos_customer_required",],
    "data": [
        "views/templates.xml",
        "views/pos_config.xml",
        "views/pos_session_view.xml",
        "views/product_template_view.xml",
        "views/pos_debt_report_view.xml",
        "views/pos_order_report.xml",
    ],
    "qweb": ["static/src/xml/templates.xml"],
    "installable": True,
}
