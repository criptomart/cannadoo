# Copyright 2021 CriptMart <tech@criptomart.net>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Stock Cannadoo",
    "version": "12.0.1.0.0",
    "author": "Criptomart",
    "category": "Warehouse",
    "summary": "Cambios en el módulo de inventario para Cannadoo \
                  1. Chatter en deseschos \
                  2. Añadido agrupamiento por PVP en análisis de inventario",
    "depends": ["stock", "stock_analysis"],
    "data": [
        "views/stock_scrap_chatter.xml",
        "views/stock_analysis_view.xml",
        "views/product_template_view.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
    "application": False,
}
