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
    'website': "http://www.yourcompany.com",

    'category': 'Services',
    'version': '15.0.1.0',

    # any module necessary for this one to work correctly
    'depends': [
                'base',
                'mail',
                'account',
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
        'security/ir.model.access.csv',

        # Sequences
        'sequences/sequence_views.xml',

        # Views
        'views/appointment.xml',
        'views/clinic.xml',
        'views/patient.xml',
        'views/doctor.xml',
        'views/sales.xml',
        # 'views/insurance.xml',
        # 'views/insurance_policy.xml',
        # 'views/medicine.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'sequence': '31',
    'license': 'LGPL-3',
    'assets': {
        'web.assets_backend': {

        },
        'web.assets_qweb': {

        },
    },
}
