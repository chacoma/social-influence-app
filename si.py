#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygtk
pygtk.require('2.0')
import gtk,sys,os
import random
import time, datetime

def cargar_preguntas(arch='sources/PREGUNTAS.txt'):
		
		f = open(arch)
		columns =[]; filas=[]
		i=0
		
		cont =0
		
		for line in f:
			if line.startswith("#"):
				None
			else:
				columns = line.split("-")
				
				filas.append(columns)
				
				filas[i][2]= float(filas[i][2])
				i+=1
		
		f.close()
		
		return filas
		
def puntaje_2(arch):
		
	f = open(arch,'r')
	
	acu= [0]*2
	acu_err=[0]*2
	cont=[0]*2 
	err_medio=[0]*2
	calificacion=[0]*2			
	
	for line in f:
		if line.startswith("#"):
			None
		else:
			col = line.split(" ")
			err= abs( 1.0 - float(col[3])/float(col[2]) )*100
			
			i= int(col[0])-1
			
			acu_err[i]+=err
			cont[i]+=1
			
			if err <= 1.0:
				acu[i]+= 100.0
			
			elif err > 1.0 and err <= 5:
				acu[i]+=50.0
				
			elif err > 5 and err <= 25.0:
				acu[i]+=25.0
				
			elif err > 25.0 and err <=125.0:
				acu[i]+=10
			
			elif err > 125:
				acu[i]+=5
				
			else:
				None
			
			
				
	f.close()
	
	i=0
	
	for i in range(2):
		
		err_medio[i]=1.0*acu_err[i]/cont[i]
		
		if acu[i]==2000:
			calificacion[i]='Excelente!'
		
		elif acu[i]>=1000:
			calificacion[i]='Muy bueno!'
		
		elif acu[i]>=500 and acu[i]<1000:
			calificacion[i]='Bien!'
		
		elif acu[i]>=200 and acu[i]<500:
			calificacion[i]='Regular'
		
		elif acu[i]<=200:
			calificacion[i]='Flojo...'
	
	
	return acu, err_medio, calificacion
				

# ENTORNO GRAFICO  \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
class Ventana:
	
	def __init__(self):
		
		# datos del jugador 1
		self.arch_jugador='archivo'
		self.user='nombre'
		self.sexo='mucho'
		self.edad='21'
		# variables del jugador
		self.respuesta_elegida=0
		self.confianza_elegida=0
		self.respuesta_correcta=0
		self.ID_pregunta=0
		self.contador_preg=0
		
		self.level=1.0
		
		self.t0=0
		self.tf=0
		
		self.txt_preguntas= cargar_preguntas()
		self.txt_preguntas_L2= cargar_preguntas()
		self.txt_preguntas_prueba= cargar_preguntas('sources/PREGUNTAS_PRUEBA.txt')
		
		self.respuestas_L1={}
		
		self.L1=len(self.txt_preguntas)
		self.L2=len(self.txt_preguntas)
		self.Lp=len(self.txt_preguntas_prueba)
		
		
		
		# VENTANA DE INICIO ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		# Creo la ventana
		self.ventana= gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.ventana.set_size_request(800, 600)
		self.ventana.set_title("SD")
		self.ventana.set_resizable(False) 
		self.ventana.show()
		self.ventana.connect("delete-event", self.win_close, None)
		
		# Creo la tabla y se la adjunto a la ventana
		self.tabla= gtk.Table(19,6,gtk.TRUE)
		self.tabla.set_row_spacings(5)
		self.tabla.set_col_spacings(5)

		self.ventana.add(self.tabla)
		
		# titulo
		titulo= gtk.Frame("")
		titulo_label = gtk.Label("")
		titulo_label.set_use_markup(True) # esto es para poder agrandar la letra
		titulo_label.set_markup('<span size="18000"> Intercambio y manejo de información</span>')
		titulo_label.set_alignment(0, 0.5)
		titulo.add(titulo_label)
		self.tabla.attach(titulo,0,6,0,2)
		
		# imagen portada
		self.image = gtk.Image()
		self.image.set_from_file("sources/fondo_chileno_2.jpg")
		self.tabla.attach(self.image,0,6,2,13)
		self.image.show()
		
		# Ubicacion de los campos y tamanhos
		nx=1-1
		ny=12+2
		w1=1
		w2=3
			
		# Creo formato inicial/ ingreso nombre ~~~~~~~~~~~~~~~~~~~~~~~~~
		user = gtk.Frame()
		user_lebel = gtk.Label("Lugar:")
		user.add(user_lebel)
		self.tabla.attach(user,nx,nx+w1,ny,ny+1)
		
		data_user = gtk.Frame()
		self.data_user =  gtk.Entry()
		self.data_user.set_max_length(12)
		self.data_user.set_text("IB-CAB")
		#self.data_user.select_region(True)
		data_user.add(self.data_user)
		self.tabla.attach(data_user,nx+w1,nx+2*w1,ny,ny+1)
		
		ny+=1
		
		# SEXO ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		sexo = gtk.Frame()
		sexo_label = gtk.Label("Sexo:")
		sexo.add(sexo_label)
		self.tabla.attach(sexo,nx,nx+w1,ny,ny+1)
		
		data_sexo = gtk.Frame()
		self.data_sexo =  gtk.Entry()
		self.data_sexo.set_max_length(1)
		self.data_sexo.set_text("M-F")
		data_sexo.add(self.data_sexo)
		self.tabla.attach(data_sexo,nx+w1,nx+2*w1,ny,ny+1)
		
		ny+=1		
		
		# EDAD ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		edad = gtk.Frame()
		edad_label = gtk.Label("Edad:")
		edad.add(edad_label)
		self.tabla.attach(edad,nx,nx+w1,ny,ny+1)
		
		data_edad = gtk.Frame()
		self.data_edad =  gtk.Entry()
		self.data_edad.set_max_length(2)
		self.data_edad.set_text("00")
		data_edad.add(self.data_edad)
		self.tabla.attach(data_edad,nx+w1,nx+2*w1,ny,ny+1)
		
		ny-=3
		# BOTONES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		ny+=1
		w1=1
		nx+=4
		'''
		self.comenzar=gtk.Button("PROBAR")
		self.comenzar.connect("clicked",self.PRUEBA)
		self.tabla.attach(self.comenzar,nx,nx+2*w1,ny,ny+w1)
		'''
		ny+=1
		
		self.comenzar=gtk.Button("COMENZAR")
		self.comenzar.connect("clicked",self.INFO_L1)
		self.tabla.attach(self.comenzar,nx,nx+2*w1,ny,ny+2*w1)
		
		ny+=2
		
		# pie de pagina
		pie= gtk.Frame("")
		pie_label = gtk.Label("")
		pie_label.set_use_markup(True) # esto es para poder agrandar la letra
		pie_label.set_markup('<span size="10000"> Por  <b>A. Chacoma + D. H. Zanette</b> //// Grupo de Física Estadística e Interdisciplinaria <b>(FiEstIn)</b> - <b>CAB</b> </span>')
		#pie_label.set_alignment(0, 0.5)
		pie.add(pie_label)
		self.tabla.attach(pie,0,6,17,19)
		
		self.ventana.show_all()	
		
		self.fecha = str(datetime.datetime.today())
		
		print "\n||||||||||||||||| Social Dynamic ||||||||||||||||||||||"
		print "[Fecha y hora de inicio: %s]" % self.fecha
		print "[Cant de preguntas: %d]" % self.L1
	
	# Funciones útiles
	def main(self):
		gtk.main()
		
	def refrescar(self):
		while gtk.events_pending():
			gtk.main_iteration()	
		
	def destroy(self, data=None):
		self.refrescar()
		gtk.main_quit()
		return False 

	def win_close(self, widget, event, data):
			dialog = gtk.MessageDialog(self.ventana, gtk.DIALOG_MODAL,
									   gtk.MESSAGE_INFO, gtk.BUTTONS_YES_NO,
									   "¿Está seguro de que quiere cerrar?")
			dialog.set_title("close?")

			response = dialog.run()
			dialog.destroy()
			if response == gtk.RESPONSE_YES:
				self.refrescar()
				gtk.main_quit()
				return False # returning False makes "destroy-event" be signalled
							 # for the window.
			else:
				return True # returning True avoids it to signal "destroy-event"
				
	# Carga todo el formato del entorno preguntas
	def set_entorno_preguntas(self, op):
		
		# VENTANA DE PREGUNTAS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		#print '[Generando entorno de preguntas ..]' 
	
		self.tabla= gtk.Table(19,8,gtk.TRUE)
		self.tabla.set_row_spacings(5)
		self.tabla.set_col_spacings(5)
		self.ventana.add(self.tabla)
		
		nx=0;	ny=2
		wx=8; 	wy=4
		
		# Creo frame de pregunta ~~~~~~~~~~~~~~~~~~~~~~~~~
		self.nro_preg= gtk.Frame("")
		self.pregunta = gtk.Label("")
		self.pregunta.set_use_markup(True) # esto es para poder agrandar la letra
		self.nro_preg.add(self.pregunta)
		self.tabla.attach(self.nro_preg,nx,nx+wx-2,ny-1,ny+wy)
		
		# Creo foto ilustrativa
		self.image_preg = gtk.Image()
		self.tabla.attach(self.image_preg,6,8,1,6)
		
		
		ny+=1+wy
		wy=wy-1
		
		self.feed= gtk.Frame("")
		self.feedback = gtk.Label("")
		self.feedback.set_use_markup(True) # esto es para poder agrandar la letra
		self.feed.add(self.feedback)
		self.tabla.attach(self.feed,nx+2,nx+wx-2,ny,ny+wy)
		
		nx+=2;		ny+=1+wy
		wx=2; 		wy=1
		
		# Creo botones respuestas ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		tu_resp= gtk.Frame()
		tu_resp_label =gtk.Label("Su respuesta:")
		tu_resp.add(tu_resp_label)
		self.tabla.attach(tu_resp,nx,nx+wx,ny,ny+wy)

		nx+=wx
		
		#///////////////////////////////////////// FRAME DE DATOS (RESPUESTA)
		RESP = gtk.Frame()
		self.RESP=  gtk.Entry()
		self.RESP.set_max_length(30)
		self.RESP.set_text("??")
		RESP.add(self.RESP)
		self.tabla.attach(RESP,nx,nx+wx,ny,ny+wy)
		#/////////////////////////////////////////
		
		nx-=2
		ny+=1
		# Creo seguridad ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		seguro= gtk.Frame()
		seguro_label=gtk.Label("Nivel de confianza:")
		seguro.add(seguro_label)
		self.tabla.attach(seguro,nx,nx+wx,ny,ny+wy)
		
		nx+=wx
		#///////////////////////////////////////// FRAME DE DATOS (CONFIANZA)
		CONF = gtk.Frame()
		self.CONF=  gtk.Entry()
		self.CONF.set_max_length(30)
		self.CONF.set_text("¿¿??")
		CONF.add(self.CONF)
		self.tabla.attach(CONF,nx,nx+wx,ny,ny+wy)
		#////////////////////////////////////////
		
		ny+=1
		
		# Creo boton RESPONDER ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		self.boton_responder=gtk.Button("Responder")
		
		if op=='pregunta_L1' or op=='pregunta_L2':
			self.boton_responder.connect("clicked",self.RESPONDER)
		
		elif op=='prueba':
			self.boton_responder.connect("clicked",self.RESPONDER_PRUEBA)
						
		self.tabla.attach(self.boton_responder,nx,nx+wx,ny,ny+wy)
		
		nx+=2
		ny+=3;	wy+=1
		
		# Creo botones de siguiente pregunta ~~~~~~~~~~~~~~~~~~~~~~~
		self.boton_sig_preg=gtk.Button("Siguiente pregunta")
		
		if op=='pregunta_L1':
			self.boton_sig_preg.connect("clicked",self.PREGUNTAS_L1)
		
		if op=='pregunta_L2':
			self.boton_sig_preg.connect("clicked",self.PREGUNTAS_L2)
		
		elif op=='prueba':
			self.boton_sig_preg.connect("clicked",self.PREGUNTAS_PRUEBA)
			
		self.tabla.attach(self.boton_sig_preg,nx,nx+wx,ny,ny+wy)
		
		nx-=4
		wx+=2
		
		# Creo frame de mensajes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		mens= gtk.Frame()
		self.mensaje=gtk.Label("")
		mens.add(self.mensaje)
		self.tabla.attach(mens,nx,nx+wx,ny,ny+wy)
	
		# agrego dibujito de confianza
		
		# imagen portada
		self.image_conf = gtk.Image()
		self.image_conf.set_from_file("sources/niveles3.png")
		self.tabla.attach(self.image_conf,0,2,6,18)
		self.image_conf.show()
	
		self.ventana.show_all()
	
	
	# FUNCIONES DE LOS BOTONES ======================================
	def RESPONDER(self, data=None):
		
		r= self.RESP.get_text()
		c= self.CONF.get_text()
		
		# chequeo que la respuesta sea un numero
		if r.replace('.','',1).isdigit() and c.isdigit() and int(c)<=5 and int(c)>=0 :
			
						
			self.boton_responder.set_sensitive(False)
			self.RESP.set_sensitive(False)
			self.CONF.set_sensitive(False)
			
			self.boton_sig_preg.set_sensitive(True)
			
			self.respuesta_elegida = float(r)
			self.confianza_elegida = int(c) 
			
			# Guardo data ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			cad= '%d %02d %.2f %.2f %d\n' % (self.level, self.ID_pregunta, self.respuesta_correcta, self.respuesta_elegida, self.confianza_elegida)
			
			#print cad
			
			f=open(self.arch_jugador, 'a')
			f.write(cad)
			f.close()
			
			# guardo en el dict para usar en el level 2
			if self.level==1:
				
				self.respuestas_L1[self.ID_pregunta]= [self.respuesta_elegida, self.confianza_elegida]
			
			self.mensaje.set_label("Por favor, continúe con la siguiente pregunta.")
			
			
		
		
		# mensajes de ERROR ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		else:
			
			mensaje='ERROR! -> '
			senhal=1
			
			if not r.replace('.','',1).isdigit():
				mensaje+= 'Su respuesta no es válida!\n'
				
			if not c.isdigit():
				mensaje+= 'No es válido el valor de confianza elegido!\n'
				senhal=0 
				
			if senhal and (int(c)>5 or int(c)<0):
				mensaje+= 'Valor de confianza fuera de rango!\n'
			
			self.mensaje.set_label("%s" % mensaje)
		
	def RESPONDER_PRUEBA(self, data=None):
		
		r= self.RESP.get_text()
		c= self.CONF.get_text()
		
		# chequeo que la respuesta sea un numero
		if r.replace('.','',1).isdigit() and c.isdigit() and int(c)<=5 and int(c)>=0 :
			
						
			self.boton_responder.set_sensitive(False)
			self.RESP.set_sensitive(False)
			self.CONF.set_sensitive(False)
			
			self.boton_sig_preg.set_sensitive(True)
			
			self.respuesta_elegida = float(r)
			self.confianza_elegida = int(c) 
			
			# NO Guardo data 
			self.mensaje.set_label("Por favor, continúe con la siguiente pregunta.")
			
			
		# mensajes de ERROR ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		else:
			
			mensaje='ERROR! -> '
			senhal=1
			
			if not r.replace('.','',1).isdigit():
				mensaje+= 'Su respuesta no es válida!\n'
				
			if not c.isdigit():
				mensaje+= 'No es válido el valor de confianza elegida!\n'
				senhal=0 
				
			if senhal and (int(c)>5 or int(c)<0):
				mensaje+= 'Valor de confianza fuera de rango!\n'
			
			self.mensaje.set_label("%s" % mensaje)
		
	
		
	def PREGUNTAS_PRUEBA(self, data=None):
		
		self.boton_sig_preg.set_sensitive(False)
		self.boton_responder.set_sensitive(True)
		self.RESP.set_sensitive(True)
		self.CONF.set_sensitive(True)
			
		self.RESP.set_text("000.00")
		self.CONF.set_text("0")

			
		L=random.randint(0, (self.Lp-1))
		pregunta=self.txt_preguntas_prueba[L]

		# aca chequeo si la pregunta tiene dos renglones
		texto= pregunta[1].split(';')
			
		if len(texto)==1:
			self.pregunta.set_markup('<span size="16000"> %s </span>' % texto[0])
		else:
			self.pregunta.set_markup('<span size="16000"> %s \n%s </span>' % (texto[0],texto[1]))
				
			
		self.contador_preg+=1
		self.nro_preg.set_label("Pregunta %d:" % self.contador_preg )
		
		self.ID_pregunta=int(pregunta[0])
		
		# foto
		self.image_preg.set_from_file("sources/%d_p.jpg" % self.ID_pregunta)
		self.image_preg.show()
			
		self.respuesta_correcta= pregunta[2]

		self.mensaje.set_label("Recuerde que su respuesta debe ser numérica.\nLos niveles de confianza van de 0 a 5.")
		
		
				
	def PREGUNTAS_L1(self, data=None):
		
		
		if not self.L1:
			self.contador_preg=0
			self.INFO_L2()				# termina las preguntas 1 paso al nivel 2
			
		else:
			
			self.boton_sig_preg.set_sensitive(False)
			self.boton_responder.set_sensitive(True)
			self.RESP.set_sensitive(True)
			self.CONF.set_sensitive(True)
			
			self.RESP.set_text("000.00")
			self.CONF.set_text("0")

			
			L=random.randint(0, (self.L1-1))
			
			pregunta=self.txt_preguntas[L]
			
			self.contador_preg+=1
			self.nro_preg.set_label("Pregunta %d:" % self.contador_preg )
			
			# aca chequeo si la pregunta tiene dos renglones
			texto= pregunta[1].split(';')
			
			if len(texto)==1:
				self.pregunta.set_markup('<span size="16000"> %s </span>' % texto[0])
			else:
				self.pregunta.set_markup('<span size="16000"> %s \n%s </span>' % (texto[0],texto[1]))
			
			
			self.respuesta_correcta= pregunta[2]
			self.ID_pregunta=int(pregunta[0])
			
			# foto
			self.image_preg.set_from_file("sources/%d.jpg" % self.ID_pregunta)
			self.image_preg.show()
				
			self.mensaje.set_label("Recuerde que su respuesta debe ser numérica.\nLos niveles de confianza van de 0 a 5.")
			
			self.txt_preguntas.pop(L)
			self.L1-=1
		
	def PREGUNTAS_L2(self, data=None):
		
		
		if not self.L2:
			self.SALIDA()				# FINALIZA
			
		else:
			
			self.boton_sig_preg.set_sensitive(False)
			self.boton_responder.set_sensitive(True)
			self.RESP.set_sensitive(True)
			self.CONF.set_sensitive(True)
			
			L=random.randint(0, (self.L2-1))
			
			pregunta=self.txt_preguntas_L2[L]
			
			self.contador_preg+=1
			self.nro_preg.set_label("Pregunta %d:" % self.contador_preg )
			
			# aca chequeo si la pregunta tiene dos renglones
			texto= pregunta[1].split(';')
			
			if len(texto)==1:
				self.pregunta.set_markup('<span size="16000"> %s </span>' % texto[0])
			else:
				self.pregunta.set_markup('<span size="16000"> %s \n%s </span>' % (texto[0],texto[1]))
			
			
			self.respuesta_correcta= pregunta[2]
			self.ID_pregunta=int(pregunta[0])
			
			#feedback 
			self.RESP.set_text("%.2f" % self.respuestas_L1[self.ID_pregunta][0])
			self.CONF.set_text("%d" % self.respuestas_L1[self.ID_pregunta][1])
			
			self.feed= pregunta[3]
			feed = pregunta[3].split(';')
			
			self.feedback.set_alignment(0.5, 0)
			
			if len(feed)==1:
				self.feedback.set_markup('<span size="12000"> %s </span>' % feed[0])
			else:
				self.feedback.set_markup('<span size="12000"> %s \n%s </span>' % (feed[0],feed[1]))
			
			
			
			# foto
			self.image_preg.set_from_file("sources/%d.jpg" % self.ID_pregunta)
			self.image_preg.show()
				
			self.mensaje.set_label("Recuerde que su respuesta debe ser numérica.\nLos niveles de confianza van de 0 a 5.")
			
			self.txt_preguntas_L2.pop(L)
			self.L2-=1
			
			
	
	def PRUEBA(self, data=None):
		
		print '[Haciendo unas preguntas de prueba ..]'
		
		self.tabla.destroy()
		
		self.set_entorno_preguntas('prueba')
		
		# Agrego el boton comenzar para poder salir del entorno preguntas y empezar a responder
		self.comenzar=gtk.Button("<- VOLVER")
		self.comenzar.connect("clicked",self.INFO_L1)
		self.tabla.attach(self.comenzar,6,8,0,1)
		
		self.ventana.show_all()	
		
		self.PREGUNTAS_PRUEBA()
		
	
	
	def INFO_L1(self, data=None):
		
		self.user=self.data_user.get_text()
		self.sexo=self.data_sexo.get_text()
		self.edad=self.data_edad.get_text()
		
		self.tabla.destroy()
		
		# VENTANA DE PREGUNTAS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		print '[Mostrando info L1]' 
	
		self.tabla= gtk.Table(19,6,gtk.TRUE)
		self.tabla.set_row_spacings(5)
		self.tabla.set_col_spacings(5)
		self.ventana.add(self.tabla)
		
		# titulo
		titulo= gtk.Frame("")
		titulo_label = gtk.Label("")
		titulo_label.set_use_markup(True) # esto es para poder agrandar la letra
		titulo_label.set_markup('<span size="18000"> Etapa 1 - Para tener en cuenta ... </span>')
		titulo_label.set_alignment(0, 0.5)
		titulo.add(titulo_label)
		self.tabla.attach(titulo,0,6,0,2)
		
		# imagen portada
		self.image = gtk.Image()
		self.image.set_from_file("sources/info.png")
		self.tabla.attach(self.image,0,6,2,13)
		self.image.show()
		
		self.comenzar=gtk.Button("HACER UNA PRUEBA")
		self.comenzar.connect("clicked",self.PRUEBA)
		self.tabla.attach(self.comenzar,4,6,14,15)
		
		self.comenzar=gtk.Button("ETAPA 1")
		self.comenzar.connect("clicked",self.LEVEL_1)
		self.tabla.attach(self.comenzar,4,6,15,17)
		
		# recomendaciones
		mensaje= '- Tómese el todo el tiempo que concidere necesario.\n- Si no sabe el valor exacto de una respuesta, intente dar un valor que usted con-\ncidere cercano.\n-Asegurese de indicar con la mayor presición posible el grado de seguridad que\nsiente respecto a la respuesta dada.'
		
		recuerde= gtk.Frame("Recomendaciones:")
		recuerde_label= gtk.Label("")
		recuerde_label.set_use_markup(True)			
		recuerde_label.set_markup('<span size="9000"> %s </span>'% mensaje)
		recuerde_label.set_alignment(0, 0.5)
		recuerde.add(recuerde_label)
		self.tabla.attach(recuerde, 0,4,13,17)
		
		
		self.ventana.show_all()			
		
	def LEVEL_1(self, data=None):
		

		# Creo archivo del jugador
		self.arch_jugador= str(int(time.time()))+ '.DAT'
		
		print '[creando archivo del jugador: %s]' % self.arch_jugador
		
		#print self.data_user.get_text()
		
		f=open(self.arch_jugador, 'w')
		f.write('# fecha= %s\n'% self.fecha)
		f.write('# lugar= %s\n'% self.user)
		f.write('# edad= %s\n'% self.edad)
		f.write('# sexo= %s\n'% self.sexo)
		f.write('# (LEVEL)(ID)(op correcta)(OP ELEGIDA)(CONF ELEGIDA)\n')
		f.close()
		
		self.tabla.destroy()
		
		self.set_entorno_preguntas('pregunta_L1')
		
		# Mando a la rutina de las preguntas	
		self.contador_preg=0
		print '[Comenzando Level 1]'
		self.PREGUNTAS_L1()
		
		
		
	def INFO_L2(self, data=None):
		
		self.tabla.destroy()
		
		# VENTANA DE PREGUNTAS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		print '[Mostrando info L2]' 
	
		self.tabla= gtk.Table(19,6,gtk.TRUE)
		self.tabla.set_row_spacings(5)
		self.tabla.set_col_spacings(5)
		self.ventana.add(self.tabla)
		
		# titulo
		titulo= gtk.Frame("")
		titulo_label = gtk.Label("")
		titulo_label.set_use_markup(True) # esto es para poder agrandar la letra
		titulo_label.set_markup('<span size="20000"> Etapa 2 - Para tener en cuenta ... </span>')
		titulo_label.set_alignment(0, 0.5)
		titulo.add(titulo_label)
		self.tabla.attach(titulo,0,6,0,2)
		
		# imagen portada
		self.image = gtk.Image()
		self.image.set_from_file("sources/info_L2.png")
		self.tabla.attach(self.image,0,6,2,13)
		self.image.show()
		'''
		self.comenzar=gtk.Button("HACER UNA PRUEBA")
		self.comenzar.connect("clicked",self.PRUEBA)
		self.tabla.attach(self.comenzar,4,6,14,15)
		'''
		self.comenzar=gtk.Button("ETAPA 2")
		self.comenzar.connect("clicked",self.LEVEL_2)
		self.tabla.attach(self.comenzar,4,6,15,17)
		
		# recomendaciones
		mensaje= '- Tómese el todo el tiempo que concidere necesario.\n- Si no sabe el valor exacto de una respuesta, intente dar un valor que usted con-\ncidere cercano.\n-Asegurese de indicar con la mayor presición posible el grado de seguridad que\nsiente respecto a la respuesta dada.'
		
		recuerde= gtk.Frame("Recomendaciones:")
		recuerde_label= gtk.Label("")
		recuerde_label.set_use_markup(True)
		recuerde_label.set_markup('<span size="9000"> %s </span>' % mensaje)
		recuerde_label.set_alignment(0, 0.5)
		recuerde.add(recuerde_label)
		self.tabla.attach(recuerde, 0,4,13,17)
		
		
		#print self.respuestas_L1
			
		self.ventana.show_all()			
		
	def LEVEL_2(self, data=None):
		
		'''
		# Creo archivo del jugador
		print '\n[creando archivo del jugador ..]'
		
		self.arch_jugador= self.user + '-' + str(int(time.time()))+ '.DAT'
		
		print self.data_user.get_text()
		
		f=open(self.arch_jugador, 'w')
		f.write('# user= %s\n'% self.user)
		f.write('# edad= %s\n'% self.edad)
		f.write('# sexo= %s\n'% self.sexo)
		f.write('# (ID)(op correcta)(OP ELEGIDA)(CONF ELEGIDA)\n')
		f.close()
		
		'''
		self.level=2.0
		
		self.tabla.destroy()
		
		self.set_entorno_preguntas('pregunta_L2')
		
		# Mando a la rutina de las preguntas	
		print '[Comenzando Level 2]'
		self.PREGUNTAS_L2()
		
		
		
	def SALIDA(self):
		
		self.tabla.destroy()
		
		print '[Mostrando puntaje..]' 
	
		self.tabla= gtk.Table(19,8,gtk.TRUE)
		self.tabla.set_row_spacings(5)
		self.tabla.set_col_spacings(5)
		self.ventana.add(self.tabla)
		
		# Creo frame de puntaje
		msj_pje_frame = gtk.Frame("")
		msj_pje_label = gtk.Label("")
		msj_pje_label.set_use_markup(True)
		msj_pje_frame.add(msj_pje_label)
		self.tabla.attach(msj_pje_frame, 1,7, 1,5)
		
		# el texto...
		msj_pje_label.set_markup(' <span size="18000"> Puntaje final:\n</span> <span size="10000">El puntaje final es calculado a partir del error relativo de\ncada respuesta dada, respecto de la respuesta correcta.</span> ')
		
		pje, err, calif = puntaje_2(self.arch_jugador)
		
		# Creo frame de puntaje
		pje_l1_frame= gtk.Frame("")
		pje_l1_label= gtk.Label("")
		pje_l1_label.set_use_markup(True)
		pje_l1_frame.add(pje_l1_label)
		self.tabla.attach(pje_l1_frame, 1,4, 5,9)
		
		pje_l1_label.set_markup(' <span size="18000"> %.2f </span>\n<span size="14000">%.2f %c er\n%s</span> ' % (pje[0], err[0],'%',calif[0]))
		
		level1_label= gtk.Label("")
		level1_label.set_use_markup(True)
		self.tabla.attach(level1_label, 1,4, 9,11)
		level1_label.set_markup(' <span size="18000">ETAPA 1</span> ')
		
		pje_l2_frame= gtk.Frame("")
		pje_l2_label= gtk.Label("")
		pje_l2_label.set_use_markup(True)
		pje_l2_frame.add(pje_l2_label)
		self.tabla.attach(pje_l2_frame, 4,7, 5,9)
		
		pje_l2_label.set_markup(' <span size="18000"> %.2f </span>\n<span size="14000">%.2f %c er\n%s</span> ' % (pje[1], err[1],'%',calif[1]))
		
		level2_label= gtk.Label("")
		level2_label.set_use_markup(True)
		self.tabla.attach(level2_label, 4,7, 9,11)
		level2_label.set_markup(' <span size="18000">ETAPA 2</span> ')
		
		# imagen portada
		imagen = gtk.Image()
		imagen.set_from_file("sources/japan_street.png")
		self.tabla.attach(imagen,1,7,11,14)
		imagen.show()
		
		#menaje final
		msj_final = gtk.Label("")
		msj_final.set_use_markup(True) # esto es para poder agrandar la letra
		self.tabla.attach(msj_final,1,5, 15,17)
	
		msj_final.set_markup('<span size="14000"> Eso fue todo,\n¡Muchas gracias por participar!... </span>')
		
		salir=gtk.Button("SALIR")
		salir.connect("clicked",self.destroy)
		self.tabla.attach(salir,5,7, 15,17)
		
		self.ventana.show_all()


		print "[Se terminó]"


# //////////////////////////////////////////////////////////////////////
if (__name__ == "__main__"):
	
	
	base= Ventana()
	base.main()
	'''
	
	print puntaje_2('1396100123.DAT')
	'''
	
	
	
