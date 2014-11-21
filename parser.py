# -----------------------------------------------------------------------------
# module: parser.py
# Parser Rules
# -----------------------------------------------------------------------------
#import tp_teleng_lex as tplex
import ply.yacc as yacc
import sys
from lexer import *
from visual import *
import numpy as np
from elemento import *

def p_programa(t):
	'programa : reglas main reglas'
	print 'programa : reglas main reglas'
	t[0] = t[2]
	t[0].mostrar()
	
def p_reglas_empty(t):
	'reglas :'
	print 'reglas :'
	pass

def p_reglas_main(t):
	'reglas : reglas main'
	print 'reglas : reglas main'

def p_reglas_unaregla(t):
	'reglas : reglas unaregla'
	print 'reglas : reglas unaregla'
	
def p_main(t):
	"main : nombremain '=' elemento"
	print "main : nombremain '=' elemento"
	t[0]=t[3]

def p_nombremain(t):
	"nombremain : '$'"
	print "nombremain : '$'"
	t[0] = t[1] 

def p_nombremain_final(t):
	"nombremain : '$' '.'"
	print "nombremain : '$' '.'"
	t[0] = t[1]+'.'

def p_unaregla(t):
	"unaregla : nombreregla '=' elemento"
	print "unaregla : nombreregla '=' elemento"
	
def p_nombreregla(t):
	'nombreregla : REGLA'
	print 'nombreregla : REGLA'

def p_nombreregla_final(t):
	"nombreregla : REGLA '.'"
	print "nombreregla : REGLA '.'"

def p_elemento(t):
	"elemento : elemento '|' elementoand"
	print "elemento : elemento '|' elementoand"
	t[0] = t[1].append(t[3])

def p_elemento_salteo(t):
	'elemento : elementoand'
	print 'elemento : elementoand'
	t[0]=ElementoOR(inicial=t[1])

def p_elementoand(t):
	"elementoand : elementoand '&' elementobase"
	t[0] = t[1].append(t[3])
	print "elementoand : elementoand '&' elementobase"

def p_elementoand_salteo(t):
	'elementoand : elementobase'
	t[0]=ElementoAND(inicial=t[1])
	print 'elementoand : elementobase'

def p_elementobase_prim(t):
	'elementobase : prim'
	t[0]=t[1]
	print 'elementobase : prim'

def p_elementobase_trans(t):
	"elementobase : elementobase ':' trans"
	t[0] = t[1].transformar(t[3])
	print "elementobase : elementobase ':' trans"

def p_elementobase_corchete(t):
	"elementobase : '[' elemento ']'"
	print "elementobase : '[' elemento ']'"

def p_elementobase_pot(t):
	"elementobase : elementobase '^' numero"
	print "elementobase : elementobase '^' numero"

def p_elementobase_maymen(t):
	"elementobase : '<' elemento '>'"
	t[0]= ElementoOR(inicial=Nada()).append(t[2])
	print "elementobase : '<' elemento '>'"

def p_elementobase_nombreregla(t):
	'elementobase : nombreregla'
	print 'elementobase : nombreregla'

def p_elementobase_nombremain(t):
	"elementobase : nombremain"
	print "elementobase : nombremain"

def p_ball(t):
	'prim : BALL'
	t[0]=Ball()
	print 'prim : BALL'

def p_box(t):
	'prim : BOX'
	t[0]=Box()
	print 'prim : BOX'

def p_nada(t):
	'prim : NADA'
	t[0]=Nada()
	print 'prim : NADA'

def p_trans_rx(t):
	'trans : RX numero'
	t[0]= TransRX(num=t[2])
	print 'trans : RX numero'

def p_trans_ry(t):
	'trans : RY numero'
	t[0]= TransRY(num=t[2])
	print 'trans : RY numero'

def p_trans_rz(t):
	'trans : RZ numero'
	t[0]= TransRZ(num=t[2])
	print 'trans : RZ numero'

def p_trans_s(t):
	'trans : S numero'
	num = t[2]
	t[0]= TransS(sx=num,sy=num,sz=num)
	print 'trans : S numero'

def p_trans_sx(t):
	'trans : SX numero'
	num = t[2]
	t[0]= TransS(sx=num)
	print 'trans : SX numero'

def p_trans_sy(t):
	'trans : SY numero'
	num = t[2]
	t[0]= TransS(sy=num)
	print 'trans : SY numero'

def p_trans_sz(t):
	'trans : SZ numero'
	num = t[2]
	t[0]= TransS(sz=num)
	print 'trans : SZ numero'

def p_trans_tx(t):
	'trans : TX numero'
	num = t[2]
	t[0]= TransT(tx=num)
	print 'trans : TX numero'

def p_trans_ty(t):
	'trans : TY numero'
	num = t[2]
	t[0]= TransT(ty=num)
	print 'trans : TY numero'

def p_trans_tz(t):
	'trans : TZ numero'
	num = t[2]
	t[0]= TransT(tz=num)
	print 'trans : TZ numero'

def p_trans_cr(t):
	'trans : CR numero'
	num = t[2]
	t[0]= TransC(cr=num)
	print 'trans : CR numero'

def p_trans_cg(t):
	'trans : CG numero'
	num = t[2]
	t[0]= TransC(cg=num)
	print 'trans : CG numero'

def p_trans_cb(t):
	'trans : CB numero'
	num = t[2]
	t[0]= TransC(cb=num)
	print 'trans : CB numero'

def p_trans_d(t):
	'trans : D numero'
	num = t[2]
	t[0]= TransD(d=num)	
	print 'trans : D numero'

def p_numero_mas_factor(t):
	"numero : numero '+' factor"
	t[0] = t[1] + t[3]

def p_numero_menos_factor(t):
	"numero : numero '-' factor"
	t[0] = t[1] - t[3]

def p_factor_por_termino(t):
	"factor : factor '*' termino"
	t[0] = t[1] * t[3]

def p_factor_div_termino(t):
	"factor : factor '/' termino"
	t[0] = t[1] / t[3]

def p_salteo(t):
	'''numero : factor
	   factor : termino
	   termino : NUM'''
	t[0] = t[1]

def p_termino_mas(t):
	"termino : '+' NUM"
	t[0] = t[2]
	print "termino : '+' NUM"

def p_termino_menos(t):
	"termino : '-' NUM"
	t[0] = -1 * t[2]
	print "termino : '-' NUM"

def p_termino_parentesis(t):
	"termino : '(' numero ')'"
	t[0] = t[2]
	print "termino : '(' numero ')'"

def p_termino_parentesis_mas(t):
	"termino : '+' '(' numero ')' "
	t[0] = t[3]
	print "termino : '+' '(' numero ')' "

def p_termino_menos(t):
	"termino : '-' '(' numero ')' "
	t[0] = -1 * t[3]
	print "termino : '-' '(' numero ')' "
	   
# Error rule for syntax errors.
def p_error(t):
	raise SyntaxError("invalid syntax")
# Build the parser.
parser = yacc.yacc()

with open(sys.argv[1], 'r') as content_file:
	content = content_file.read()
#print content
result = parser.parse(content)
print result