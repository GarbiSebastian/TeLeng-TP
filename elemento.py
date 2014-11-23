import sys
import numpy as np
from visual import *
import random as aleatorio
from transformacion import *
import copy

class Elemento(object):
	def transformar(self,trans):
		return self

	def mostrar(self):
		pass

	def debug(self):
		pass

	def getTrans(self):
		return []

	def getElemento(self):
		return self

	def aplicarTrans(self):
		pass
#------------------------------------------------------------------------
class Primitiva(Elemento):
	def __init__(self):
		self.estado = Transformacion()
		self.orig = None
		self.dirx = None
		self.diry = None
		self.dirz = None
		self.size = None

	def transformar(self,trans):
		self.estado.transformar(trans)
		return self

	def mostrar(self):
		trans = self.estado
		if self.orig is None:
			self.orig = np.dot([0,0,0,1], trans.space)[:3]
			self.dirx = np.dot([1,0,0,0], trans.space)[:3]
			self.diry = np.dot([0,1,0,0], trans.space)[:3]
			self.dirz = np.dot([0,0,1,0], trans.space)[:3] 
			self.size = [np.linalg.norm(self.dirx),np.linalg.norm(self.diry),np.linalg.norm(self.dirz)]

	def debug(self):
		self.estado.debug()
		print "self.orig"
		print self.orig
		print "self.dirx"
		print self.dirx
		print "self.diry"
		print self.diry
		print "self.dirz"
		print self.dirz
		print 'self.size'
		print self.size
#------------------------------------------------------------------------
class Ball(Primitiva):
	def mostrar(self):
		super(Ball,self).mostrar()
		#self.debug()
		ellipsoid(pos=self.orig,size=self.size,axis=self.dirx,up=self.diry,color=self.estado.color)
#------------------------------------------------------------------------
class Box(Primitiva):
	def mostrar(self):
		super(Box,self).mostrar()
		#self.debug()
		box(pos=self.orig,size=self.size,axis=self.dirx,up=self.diry,color=self.estado.color)
#------------------------------------------------------------------------
class Nada(Primitiva):
	def mostrar(self):
		#self.debug()
		pass
#------------------------------------------------------------------------
class Compuesta(Elemento):
	def __init__(self):
		self.elementos = []
		
	def append(self,elemento):
		self.elementos.append(elemento)
		return self
	
	def transformar(self,trans):
		for elem in self.elementos:
			elem.transformar(trans)
		return self
		
	def debug(self):
		for (i, item) in enumerate(items):
			item.debug()
#------------------------------------------------------------------------
class ElementoAND(Compuesta):
	def mostrar(self):
		for elem in self.elementos:
			elem.mostrar()
#------------------------------------------------------------------------
class ElementoOR(Compuesta):
	def mostrar(self):
		size = len(self.elementos)
		elem = self.elementos[aleatorio.randrange(0, size, 1)]
		elem.mostrar()

#------------------------------------------------------------------------
class ElementoPOT(Elemento):
	def __init__(self,elemento,numero):
		self.elemento = elemento
		self.numero = numero

	def obtener(self):
		ret = ElementoAND()
		e = self.elemento.getElemento()
		ts = self.elemento.getTrans()
		n = self.numero
		while n > 0:
			ret.append(copy.deepcopy(e))
			for t in ts:
				ret.transformar(t)
			n -= 1
		return ret

class ElementoCorchete(Elemento):
	def __init__(self,elemento):
		self.elemento = elemento
		self.transformaciones = []

	def transformar(self, trans):
		self.transformaciones.append(trans)
		return self

	def getTrans(self):
		return self.transformaciones

	def getElemento(self):
		return self.elemento

	def aplicarTrans(self):
		for t in self.transformaciones:
			self.elemento.transformar(t)

	def mostrar(self):
		self.aplicarTrans()
		self.elemento.mostrar()

class ElementoREGLA(Elemento):
	def __init__(self,nombre,reglas,finales):
		self.nombre = nombre
		self.reglas = reglas
		self.finales = finales
		self.transformaciones = []
		self.depth = 100

	def transformar(self,trans):
		if trans.esD():
			if trans.nombre is None or trans.nombre == self.nombre: 
				self.depth = min(self.depth, trans.depth)
				trans.depth = self.depth - 1
				trans.nombre = self.nombre
		self.transformaciones.append(trans)
		return self

	def mostrar(self):
		original = self.reglas[self.nombre]
		if self.depth > 0:
			copia = copy.deepcopy(original)
			for t in self.transformaciones:
				copia.transformar(t)
			td = TransD(self.depth-1)
			td.nombre = self.nombre
			copia.transformar(td)
			copia.mostrar()
		else:
			pass

# ba = Ball()
# bo = Box()
# elemOR = ElementoOR(ba).append(bo)
# t = TransC(cb=0.5)
# #elemOR.transformar(t).mostrar()
# t2 = TransD
# t3 = t2(d=10)
# #t3.debug()

# print +-(8*5)