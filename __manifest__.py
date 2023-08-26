# -*- coding: utf-8 -*-

{
    'name': 'Hospital and Clinic Management',

    'summary': """
        Organize Hospital and Clinic services and provide Patient Reports .
        """,

    'description': """
        Hospital and Clinic Management
    """,

    'author': "Mohamed Sobh",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Services',
    'version': '15.0.0',

    # any module necessary for this one to work correctly
    'depends': ['stock',
                'base',
                'mail',
                'l10n_eg',
                'account',
                'uom',
                'product',
                'sale',
                'sale_management',
                'purchase',
                'hr_expense',
                'web_kanban_gauge',
                ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',

        # Sequences
        'sequences/sequence_views.xml',
        
        # Views
        'views/clinic.xml',
        'views/patient.xml',
        # 'views/appointment.xml',
        # 'views/doctor.xml',
        # 'views/insurance.xml',
        # 'views/insurance_policy.xml',
        # 'views/medicine.xml',
        
        # 'views/pharmacist.xml',
        # 'views/staff.xml',
        # 'views/transaction.xml',
        
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
