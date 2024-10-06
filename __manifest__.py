# -*- coding: utf-8 -*-

{
    'name': 'Hospital and Clinic Management',

    'summary': """
        Organize Hospital and Clinic services and provide Patient Reports .
        """,

    'description': """
        Hospital and Clinic Management System
    """,

    'author': "Mohamed Sobh",
    "website": "https://info.odoo-express.com",
    'license': 'OPL-1',
    'price': 49.99,
    'currency': 'EUR',

    'category': 'Services',
    'version': '17.0.1.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'mail',
        'account',
        'analytic',
        'stock',
        'l10n_eg',
        'uom',
        'product',
        'sale',
        'sale_management',
        'purchase',
        'hr',
        'hr_expense',
        'web_kanban_gauge',
        'portal',
        'web',
        'calendar',
    ],
    # always loaded
    'data': [
        # Security
        'security/ir.model.access.csv',

        # 'security/security.xml',
        # Data
        # 'data/data_company.xml',
        'data/data_records.xml',
        'data/data_mail_action.xml',
        # Sequences
        'sequences/sequence_views.xml',
        # reports and Menu
        'reports/menu.xml',
        'reports/ticket_report.xml',
        # wizard
        'wizard/reschedule_ticket.xml',
        # Views
        'views/clinics.xml',
        'views/rooms.xml',
        'views/staff.xml',
        'views/patients.xml',
        'views/services.xml',
        # 'views/sales.xml',
        # 'views/insurance.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'sequence': 46,
    'assets': {
        'web.assets_backend': {
            'ms_hospital/static/scr/js/feature.js',
        },
        'web.assets_frontend': {

        },
        'web.assets_qweb': {

        },
    },
}
