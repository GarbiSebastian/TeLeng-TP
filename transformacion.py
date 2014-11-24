import sys
import numpy as np
from math import *
from copy import deepcopy

class Transformacion(object):
	def __init__(self):
		self.space = np.identity(4)
		self.color = np.array([1,1,1])
		self.depth = 100
		
	def transformar(self,trans):
		self.space = np.dot(self.space,trans.space)
		self.color = self.color * trans.color
		self.depth = min(self.depth, trans.depth)

	def debug(self):
		print 'space'
		print self.space
		print 'color'
		print self.color
		print 'depth'
		print self.depth
#------------------------------------------------------------------------
class TransRX(Transformacion):
	def __init__(self,num):
		super(TransRX,self).__init__()
		x = radians(num)
		self.space = np.array([[1, 0, 0, 0],[0, cos(x), sin(x), 0],[0, -sin(x), cos(x), 0],[0, 0, 0, 1]])

class TransRY(Transformacion):
	def __init__(self,num):
		super(TransRY,self).__init__()
		y = radians(num)
		self.space = np.array([[cos(y), 0, -sin(y), 0],[0, 1, 0, 0],[sin(y), 0, cos(y), 0],[0, 0, 0, 1]])

class TransRZ(Transformacion):
	def __init__(self,num):
		super(TransRZ,self).__init__()
		z = radians(num)
		self.space = np.array([[cos(z), sin(z), 0, 0],[-sin(z), cos(z), 0, 0],[0, 0, 1, 0],[0, 0, 0, 1]])

class TransT(Transformacion):
	def __init__(self,tx=0,ty=0,tz=0):
		super(TransT,self).__init__()
		self.space = np.array([[1, 0, 0, 0],[0, 1, 0, 0],[0, 0, 1, 0],[tx, ty, tz, 1]])

class TransS(Transformacion):
	def __init__(self,sx=1,sy=1,sz=1):
		super(TransS,self).__init__()
		self.space = np.array([[sx, 0, 0, 0],[0, sy, 0, 0],[0, 0, sz, 0],[0, 0, 0, 1]])

class TransC(Transformacion):
	def __init__(self,cr=1,cg=1,cb=1):
		super(TransC,self).__init__()
		self.color = np.array([cr, cg, cb])

class TransD(Transformacion):
	def __init__(self,d=100):
		super(TransD,self).__init__()
		self.depth = d