# -*- coding: utf-8 -*-
from openerp import models, fields, api

class parking(models.Model):
	_name = 'parking.parking'

class plaza(models.Model):
	_name = 'parking.plaza'
	numero = fields.Char(string="Nombre de la plaza", required=True)
	planta = fields.Selection([
        ('1', "Planta 1 (Dirección y visitas)"),
        ('2', "Planta 2 (Empleados Metalasa)"),
        ('3', "Planta 3 (Empleados externos)"),
    ], default='1')
	disponible = fields.Boolean(string="Disponible")
	usuario = fields.Many2one('res.users')
	
