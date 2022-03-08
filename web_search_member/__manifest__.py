# Copyright 2021 Criptomart <tech@criptomart.net>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Website Search Member",
    "summary": "Adds a website form to search a member",
    "version": "12.0.1.0.1",
    "category": "Membership",
    "author": "Criptomart",
    "website": "https://criptomart.net",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "membership",
        "website"
    ],
    "data": [
        "data/menu.xml",
        "views/web_templates.xml"
    ],
}
