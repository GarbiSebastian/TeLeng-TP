import numpy as num
import math

class Transformacion(object):
	def __init__(self):
		self.space = num.identity(4)
		self.color = num.array([1,1,1])
		self.depth = 100

	def transformar(self,trans):
		self.space = num.dot(self.space,trans.space)
		self.color = self.color * trans.color
		self.depth = min(self.depth, trans.depth)

	def debug(self):
		print self.space
		print self.color
		print self.depth
#------------------------------------------------------------------------

class TransRX(Transformacion):
	def __init__(self,num):
		super(TransRX,self).__init__()
		x = math.radians(num)
		self.space = num.matrix([[1, 0, 0, 0],[0, cos(X), sin(x), 0],[0, -sin(X), cos(x), 0],[0, 0, 0, 1]])

class TransRY(Transformacion):
	def __init__(self,num):
		super(TransRY,self).__init__()
		y = math.radians(num)
		self.space = num.matrix([[cos(y), 0, -sin(y), 0],[0, 1, 0, 0],[sin(y), 0, cos(y), 0],[0, 0, 0, 1]])

class TransRZ(Transformacion):
	def __init__(self,num):
		super(TransRZ,self).__init__()
		z = math.radians(num)
		self.space = num.matrix([[cos(z), sin(z), 0, 0],[-sin(z), cos(z), 0, 0],[0, 0, 1, 0][0, 0, 0, 1]])

class TransT(Transformacion):
	def __init__(self,tx=0,ty=0,tz=0):
		super(TransT,self).__init__()
		self.space = num.matrix([[1, 0, 0, 0],[0, 1, 0, 0],[0, 0, 1, 0][tx, ty, tz, 1]])

class TransS(Transformacion):
	def __init__(self,sx=0,sy=0,sz=0):
		super(TransS,self).__init__()
		self.space = num.matrix([[sx, 0, 0, 0],[0, sy, 0, 0],[0, 0, sz, 0][0, 0, 0, 1]])

class TransC(Transformacion):
	def __init__(self,cr=1,cg=1,cb=1):
		super(TransC,self).__init__()
		self.color = num.array([cr, cg, cb])

class TransD(Transformacion):
	def __init__(self,d=100):
		super(TransD,self).__init__()
		self.depth = d