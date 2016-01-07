# -*- coding: utf-8 -*-
{
    'name': "Parking",

    'summary': """
        Gestión de las plazas de parking de la empresa""",

    'description': """Módulo básico para gestionar las plazas de parking del aparcamiento de la empresa. 
	El usuario reserva plaza entre las disponibles y la devuelve cuando ya no la necesita
    """,

    'author': "Xavier Meler",
    'website': "http://skills.cat",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Herramientas extra',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
		'security/ir.model.access.csv',
		'views/plazas.xml',
		'views/reservas.xml',
		'templates.xml',
    ],    
    
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}