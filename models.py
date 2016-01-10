# -*- coding: utf-8 -*-
from openerp import models, fields, api
import time

from openerp.exceptions import Warning

class parking(models.Model):
	_name = 'parking.parking'

class plaza(models.Model):
	_name = 'parking.plaza'
	_rec_name ='numero'
	numero = fields.Char(string="Número de la plaza", required=True)
	planta = fields.Selection([
        ('1', "Planta 1 (Dirección y visitas)"),
        ('2', "Planta 2 (Empleados Metalasa)"),
        ('3', "Planta 3 (Empleados externos)"),
    ], default='1')
	disponible = fields.Boolean(compute='_comprueba_disponibilidad')
	reserva_ids = fields.One2many(
        'parking.reserva', 'numero_id', string="Plaza")
		
	@api.one
	def _comprueba_disponibilidad (self):
		hoy = time.strftime("%Y-%m-%d")
		if self.env['parking.reserva'].search_count(
			['&',
			('numero_id','=',self.numero),
			('fecha_inicio',"<=",hoy),
			('fecha_fin',">=",hoy)
			]) > 0:
			self.disponible = False
		else:
			self.disponible = True

class reserva(models.Model) :
	_name = 'parking.reserva'
	_rec_name = 'usuario_id'
	numero_id = fields.Many2one('parking.plaza',required=True)
	usuario_id = fields.Many2one('res.users',required=True)
	fecha_inicio = fields.Date(required=True)
	fecha_fin = fields.Date(required=True)
	
	@api.one
	@api.constrains('fecha_inicio', 'fecha_fin')
	def _check_fechas(self):
		if self.fecha_inicio > self.fecha_fin:
			raise Warning("La fecha de fin debe ser posterior a la fecha de inicio")
	
	@api.model
	def create(self, values):
		warningMessage =""
		crearReserva = True
		# recuperamos los valores del formulario (se guardan en "values")
		numero_id    = values.get('numero_id')
		usuario_id   = values.get('usuario_id')
		fecha_inicio = values.get('fecha_inicio')
		fecha_fin    = values.get('fecha_fin')
		
		#comprueba que el usuario no tiene plaza de parking para esas fechas (solo una plaza a la vez)
		if self.search_count(\
			['&',('usuario_id','=',usuario_id),\
			'|','|','|',\
			'&',('fecha_inicio','>=',fecha_inicio),('fecha_inicio','<=',fecha_fin),\
			'&',('fecha_fin',   '>=',fecha_inicio),('fecha_fin',   '<=',fecha_fin),\
			'&',('fecha_inicio','<=',fecha_inicio),('fecha_fin',   '>=',fecha_inicio),\
			'&',('fecha_inicio','<=',fecha_fin),   ('fecha_fin',   '>=',fecha_fin)\
			]) > 0:
			crearReserva = False
			warningMessage += "-El usuario ya tiene plaza para esas fechas\n"
		
		#comprueba que la plaza no esta ocupada para esas fechas
		if self.search_count(\
			['&',('numero_id','=',values['numero_id']),\
			'|','|','|',\
			'&',('fecha_inicio','>=',fecha_inicio),('fecha_inicio','<=',fecha_fin),\
			'&',('fecha_fin',   '>=',fecha_inicio),('fecha_fin',   '<=',fecha_fin),\
			'&',('fecha_inicio','<=',fecha_inicio),('fecha_fin',   '>=',fecha_inicio),\
			'&',('fecha_inicio','<=',fecha_fin),   ('fecha_fin',   '>=',fecha_fin)\
			]) > 0:
			crearReserva = False
			warningMessage += "-Plaza ocupada en esas fechas"
		
		if crearReserva : 
			res_id = super(reserva, self).create(values)
			return res_id
		else:
			raise Warning(warningMessage)
			return self
			
	@api.multi
	def write(self,values):
		warningMessage = ""
		reservaOK = True
		
		# self contiene los valores almacenados (antes de actualizar) y 
		# "values" contiene los valores que han cambiado (del formulario)
		
		numero_id = values.get('numero_id');
		if not numero_id:
			numero_id = self.numero_id.id
			
		usuario_id = values.get('usuario_id');
		if not usuario_id:
			usurio_id = self.usuario_id.id
		
		fecha_inicio = values.get('fecha_inicio');
		if not fecha_inicio:
			fecha_inicio = self.fecha_inicio
		
		fecha_fin = values.get('fecha_fin');
		if not fecha_fin:
			fecha_fin = self.fecha_fin
		
		
		# comprueba que el usuario no tiene plaza de parking para esas fechas (solo una plaza a la vez)
		# no se tiene en cuenta el propio registro (colisionaria siempre)
		if self.search_count([\
			'&',('id','!=',self.id),
			'&',('usuario_id','=',usuario_id),\
			'|','|','|',\
			'&',('fecha_inicio','>=',fecha_inicio),('fecha_inicio','<=',fecha_fin),\
			'&',('fecha_fin','>=',fecha_inicio),('fecha_fin','<=',fecha_fin),\
			'&',('fecha_inicio','<=', fecha_inicio),('fecha_fin','>=',fecha_inicio),\
			'&',('fecha_inicio','<=',fecha_fin),('fecha_fin','>=',fecha_fin)\
			]) > 0:
			reservaOK = False
			warningMessage += "-El usuario ya tiene plaza para esas fechas\n"
		
		# comprueba que la plaza no esta ocupada para esas fechas
		# no se tiene en cuenta el propio registro (colisionaria siempre)
		if self.search_count([\
			'&',('id','!=',self.id),
			'&',('numero_id','=',numero_id),\
			'|','|','|',\
			'&',('fecha_inicio','>=',fecha_inicio),('fecha_inicio','<=',fecha_fin),\
			'&',('fecha_fin','>=',fecha_inicio),('fecha_fin','<=',fecha_fin),\
			'&',('fecha_inicio','<=', fecha_inicio),('fecha_fin','>=',fecha_inicio),\
			'&',('fecha_inicio','<=',fecha_fin),('fecha_fin','>=',fecha_fin)\
			]) > 0:
			reservaOK = False
			warningMessage += "-Plaza ocupada en esas fechas"
			
		if reservaOK: 
			res_id = super(reserva, self).write(values)
			return res_id
		else:
			raise Warning(warningMessage)
			return self
			
	