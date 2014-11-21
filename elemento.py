import sys
import numpy as num
from visual import *
import random as aleatorio
from transformacion import *

class Elemento(object):
	def transformar(self,trans):
		pass

	def mostrar(self):
		pass

	def debug(self):
		pass
#------------------------------------------------------------------------
class Primitiva(Elemento):
	def __init__(self):
		self.estado = Transformacion()
		self.orig = ''
		self.dirx = ''
		self.diry = ''
		self.dirz = ''
		self.size = ''

	def transformar(self,trans):
		self.estado.transformar(trans)
		return self

	def mostrar(self):
		trans = self.estado
		self.orig = num.dot([0,0,0,1], trans.space)[:3]
		self.dirx = num.dot([1,0,0,0], trans.space)[:3]
		self.diry = num.dot([0,1,0,0], trans.space)[:3]
		self.dirz = num.dot([0,0,1,0], trans.space)[:3] 
		self.size = [num.linalg.norm(self.dirx),num.linalg.norm(self.diry),num.linalg.norm(self.dirz)]

	def debug(self):
		self.estado.debug()
		print self.orig
		print self.dirx
		print self.diry
		print self.dirz
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
		self.elementos = []
		#self.elementos.append(inicial)

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

class ElementoPOT(Compuesta):
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