import sys
import numpy as np
from visual import *
import random as aleatorio
from transformacion import *
from copy import deepcopy

class Elemento(object):
	def __init__(self):
		self.estado = Transformacion()

	def transformar(self,trans):
		self.estado.transformar(trans)
		return self

	def mostrar(self):
		pass

	def debug(self):
		pass

	def getTrans(self):
		return Transformacion()

	def getElemento(self):
		return self
#------------------------------------------------------------------------
class Primitiva(Elemento):
	def __init__(self):
		super(Primitiva,self).__init__()
		self.orig = None
		self.dirx = None
		self.diry = None
		self.dirz = None
		self.size = None

	def mostrar(self):
		trans = self.estado
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
		ellipsoid(pos=self.orig,size=self.size,axis=self.dirx,up=self.diry,color=self.estado.color)
#------------------------------------------------------------------------
class Box(Primitiva):
	def mostrar(self):
		super(Box,self).mostrar()
		box(pos=self.orig,size=self.size,axis=self.dirx,up=self.diry,color=self.estado.color)
#------------------------------------------------------------------------
class Nada(Primitiva):
	def mostrar(self):
		pass
#------------------------------------------------------------------------
class Compuesta(Elemento):
	def __init__(self):
		super(Compuesta,self).__init__()
		self.elementos = []
		
	def append(self,elemento):
		self.elementos.append(elemento)
		return self
	
	def debug(self):
		for (i, item) in enumerate(items):
			item.debug()
#------------------------------------------------------------------------
class ElementoAND(Compuesta):
	def mostrar(self):
		for elem in self.elementos:
			elem.transformar(self.estado).mostrar()
#------------------------------------------------------------------------
class ElementoANDTransformaDirecto(Compuesta):
	def transformar(self,trans):
		for e in self.elementos:
			e.transformar(trans)
		return self

	def mostrar(self):
		for elem in self.elementos:
			elem.mostrar()
#------------------------------------------------------------------------
class ElementoOR(Compuesta):
	def mostrar(self):
		size = len(self.elementos)
		elem = self.elementos[aleatorio.randrange(0, size, 1)]
		elem.transformar(self.estado).mostrar()
#------------------------------------------------------------------------
class ElementoPOT(Elemento):
	def __init__(self,elemento,numero):
		super(ElementoPOT,self).__init__()
		self.elemento = elemento
		self.numero = numero

	def obtener(self):
		ret = ElementoANDTransformaDirecto()
		e = self.elemento.getElemento()
		t = self.elemento.getTrans()
		n = self.numero
		while n > 0:
			ret.append(deepcopy(e))
			ret.transformar(t)
			n -= 1
		return ret
#------------------------------------------------------------------------
class ElementoCorchete(Elemento):
	def __init__(self,elemento):
		super(ElementoCorchete,self).__init__()
		self.elemento = elemento

	def getTrans(self):
		return self.estado

	def getElemento(self):
		return self.elemento

	def mostrar(self):
		self.elemento.transformar(self.estado)
		self.elemento.mostrar()
#------------------------------------------------------------------------
class ElementoREGLA(Elemento):
	def __init__(self,nombre,reglas,finales):
		super(ElementoREGLA,self).__init__()
		self.nombre = nombre
		self.reglas = reglas
		self.finales = finales

	def getOriginal(self):
		d = self.estado.depth
		if d + 1 > 0:
			if d > 0:
				return self.reglas[self.nombre]
			else:
				return self.finales.get(self.nombre,self.reglas[self.nombre])

	def mostrar(self):
		d = self.estado.depth
		if d + 1 > 0:
			copia = deepcopy(self.getOriginal())
			copia.transformar(self.estado)
			copia.transformar(TransD(d - 1))
			copia.mostrar()
		else:
			pass

	def __deepcopy__(self,memo):
		result = ElementoREGLA(self.nombre,self.reglas,self.finales)
		setattr(result, "estado", deepcopy(self.estado, memo))
		return result
