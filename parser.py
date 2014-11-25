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

mostrarTokens = False
mostrarEjes = False
mostrarProducciones = False

with open(sys.argv[1], 'r') as content_file:
	content = content_file.read()

if mostrarTokens:
	lexer.input(content)
	while True:
		tok = lexer.token()
		if not tok:
			break
		print tok

if mostrarEjes:
	cylinder(pos=(-5,0,0), axis=(10,0,0), radius=0.01,color=color.red) #eje X
	cylinder(pos=(0,-5,0), axis=(0,10,0), radius=0.01,color=color.green) #eje Y
	cylinder(pos=(0,0,-5), axis=(0,0,10), radius=0.01,color=color.blue) #eje Z

reglas  = {}
finales = {}
verificar = []

def verificarReglas():
	for reg in verificar:
		if reg not in reglas:
			p_error()

def p_programa(t):
	'programa : reglas main masreglas'
	if mostrarProducciones:
		print 'Programa -> Reglas Main Masreglas'
	verificarReglas()
	reglas['$'].mostrar()
	
def p_reglas_empty(t):
	'reglas :'
	if mostrarProducciones:
		print 'Reglas -> LAMBDA'
	pass

def p_masreglas_empty(t):
	'masreglas :'
	if mostrarProducciones:
		print 'Masreglas -> LAMBDA'
	pass

def p_reglas_unaregla(t):
	'reglas : reglas unaregla'
	if mostrarProducciones:
		print 'Reglas -> Reglas Unaregla'

def p_masreglas_unaregla(t):
	'masreglas : masreglas unaregla'
	if mostrarProducciones:
		print 'Masreglas -> Masreglas Unaregla'

def p_masreglas_main(t):
	'masreglas : masreglas main'
	if mostrarProducciones:
		print 'Masreglas : Masreglas Main'
	
def p_unaregla(t):
	"unaregla : REGLA '=' elemento"
	reglas[t[1]] = reglas.get(t[1],ElementoOR()).append(t[3])
	if mostrarProducciones:
		print 'Unaregla -> REGLA = Elemento'

def p_main(t):
	"main : '$' '=' elemento"
	reglas[t[1]] = reglas.get(t[1],ElementoOR()).append(t[3])
	if mostrarProducciones:
		print 'Main -> $ = Elemento'

def p_unaregla_final(t):
	"unaregla : REGLA '.' '=' elemento"
	reglas[t[1]] = reglas.get(t[1],ElementoOR()).append(t[4])
	finales[t[1]] = finales.get(t[1],ElementoOR()).append(t[4])
	if mostrarProducciones:
		print 'Unaregla -> REGLA. = Elemento'

def p_main_final(t):
	"main : '$' '.' '=' elemento"
	reglas[t[1]] = reglas.get(t[1],ElementoOR()).append(t[4])
	finales[t[1]] = finales.get(t[1],ElementoOR()).append(t[4])
	if mostrarProducciones:
		print 'Main -> $. = Elemento'

def p_elemento(t):
	"elemento : elemento '|' elementoand"
	if mostrarProducciones:
		print "Elemento -> Elemento | Elementoand"
	t[0] = t[1].append(t[3])

def p_elemento_salteo(t):
	'elemento : elementoand'
	if mostrarProducciones:
		print 'Elemento -> Elementoand'
	t[0]=ElementoOR().append(t[1])

def p_elementoand(t):
	"elementoand : elementoand '&' elementobase"
	t[0] = t[1].append(t[3])
	if mostrarProducciones:
		print "Elementoand -> Elementoand & Elementobase"

def p_elementoand_salteo(t):
	'elementoand : elementobase'
	t[0]=ElementoAND().append(t[1])
	if mostrarProducciones:
		print 'Elementoand -> Elementobase'

def p_elementobase_prim(t):
	'elementobase : prim'
	t[0]=t[1]
	if mostrarProducciones:
		print 'Elementobase -> Prim'

def p_elementobase_trans(t):
	"elementobase : elementobase ':' trans"
	t[0] = t[1].transformar(t[3])
	if mostrarProducciones:
		print "Elementobase -> Elementobase : Trans"

def p_elementobase_corchete(t):
	"elementobase : '[' elemento ']'"
	t[0] = ElementoCorchete(t[2])
	if mostrarProducciones:
		print "Elementobase -> [Elemento]"

def p_elementobase_pot(t):
	"elementobase : elementobase '^' numero"
	t[0] = ElementoPOT(elemento=t[1],numero=t[3]).obtener()
	if mostrarProducciones:
		print "Elementobase -> Elementobase^Numero"

def p_elementobase_maymen(t):
	"elementobase : '<' elemento '>'"
	t[0]= ElementoOR().append(Nada()).append(t[2])
	if mostrarProducciones:
		print "Elementobase -> <Elemento>"

def p_elementobase_regla(t):
	"elementobase : REGLA"
	verificar.append(t[1])
	t[0] = ElementoREGLA(nombre=t[1],reglas=reglas,finales=finales)
	if mostrarProducciones:
		print 'Elementobase -> REGLA'

def p_elementobase_main(t):
	"elementobase : '$' "
	verificar.append(t[1])
	t[0] = ElementoREGLA(nombre=t[1],reglas=reglas,finales=finales)
	if mostrarProducciones:
		print 'Elementobase -> $'

def p_ball(t):
	'prim : BALL'
	t[0]=Ball()
	if mostrarProducciones:
		print 'Prim -> BALL'

def p_box(t):
	'prim : BOX'
	t[0]=Box()
	if mostrarProducciones:
		print 'Prim -> BOX'

def p_nada(t):
	'prim : NADA'
	t[0]=Nada()
	if mostrarProducciones:
		print 'Prim -> NADA'

def p_trans_rx(t):
	'trans : RX numero'
	t[0]= TransRX(num=t[2])
	if mostrarProducciones:
		print 'Trans -> RX Numero'

def p_trans_ry(t):
	'trans : RY numero'
	t[0]= TransRY(num=t[2])
	if mostrarProducciones:
		print 'Trans -> RY Numero'

def p_trans_rz(t):
	'trans : RZ numero'
	t[0]= TransRZ(num=t[2])
	if mostrarProducciones:
		print 'Trans -> RZ Numero'

def p_trans_s(t):
	'trans : S numero'
	num = t[2]
	t[0]= TransS(sx=num,sy=num,sz=num)
	if mostrarProducciones:
		print 'Trans -> S Numero'

def p_trans_sx(t):
	'trans : SX numero'
	num = t[2]
	t[0]= TransS(sx=num)
	if mostrarProducciones:
		print 'Trans -> SX Numero'

def p_trans_sy(t):
	'trans : SY numero'
	num = t[2]
	t[0]= TransS(sy=num)
	if mostrarProducciones:
		print 'Trans -> SY Numero'

def p_trans_sz(t):
	'trans : SZ numero'
	num = t[2]
	t[0]= TransS(sz=num)
	if mostrarProducciones:
		print 'Trans -> SZ Numero'

def p_trans_tx(t):
	'trans : TX numero'
	num = t[2]
	t[0]= TransT(tx=num)
	if mostrarProducciones:
		print 'Trans -> TX Numero'

def p_trans_ty(t):
	'trans : TY numero'
	num = t[2]
	t[0]= TransT(ty=num)
	if mostrarProducciones:
		print 'Trans -> TY Numero'

def p_trans_tz(t):
	'trans : TZ numero'
	num = t[2]
	t[0]= TransT(tz=num)
	if mostrarProducciones:
		print 'Trans -> TZ Numero'

def p_trans_cr(t):
	'trans : CR numero'
	num = t[2]
	t[0]= TransC(cr=num)
	if mostrarProducciones:
		print 'Trans -> CR Numero'

def p_trans_cg(t):
	'trans : CG numero'
	num = t[2]
	t[0]= TransC(cg=num)
	if mostrarProducciones:
		print 'Trans -> CG Numero'

def p_trans_cb(t):
	'trans : CB numero'
	num = t[2]
	t[0]= TransC(cb=num)
	if mostrarProducciones:
		print 'Trans -> CB Numero'

def p_trans_d(t):
	'trans : D numero'
	num = t[2]
	t[0]= TransD(d=num)	
	if mostrarProducciones:
		print 'Trans -> D Numero'

def p_numero_mas_factor(t):
	"numero : numero '+' factor"
	t[0] = t[1] + t[3]
	if mostrarProducciones:
		print "Numero -> Numero + Factor"


def p_numero_menos_factor(t):
	"numero : numero '-' factor"
	t[0] = t[1] - t[3]
	if mostrarProducciones:
		print "Numero -> Numero - Factor"


def p_factor_por_termino(t):
	"factor : factor '*' termino"
	t[0] = t[1] * t[3]
	if mostrarProducciones:
		print "Factor -> Factor * Termino"


def p_factor_div_termino(t):
	"factor : factor '/' termino"
	t[0] = t[1] / t[3]
	if mostrarProducciones:
		print "Factor -> Factor / Termino"

def p_salteo_n(t):
	'numero : factor'
	t[0] = t[1]
	if mostrarProducciones:
		print 'Numero -> Factor'

def p_salteo_f(t):
	'factor : termino'
	t[0] = t[1]
	if mostrarProducciones:
		print 'Factor -> Termino'

def p_salteo_t(t):
	'termino : NUM'
	t[0] = t[1]
	if mostrarProducciones:
		print 'Termino -> NUM'

def p_termino_mas(t):
	"termino : '+' NUM"
	t[0] = t[2]
	if mostrarProducciones:
		print 'Termino -> + NUM'


def p_termino_menos(t):
	"termino : '-' NUM"
	t[0] = -1 * t[2]
	if mostrarProducciones:
		print 'Termino -> - NUM'

def p_termino_parentesis(t):
	"termino : '(' numero ')'"
	t[0] = t[2]
	if mostrarProducciones:
		print 'Termino -> ( Numero )'

def p_termino_parentesis_mas(t):
	"termino : '+' '(' numero ')' "
	t[0] = t[3]
	if mostrarProducciones:
		print 'Termino -> + ( Numero )'

def p_termino_parentesis_menos(t):
	"termino : '-' '(' numero ')' "
	t[0] = -1 * t[3]
	if mostrarProducciones:
		print 'Termino -> - ( Numero )'
	   
# Error rule for syntax errors.
def p_error(t):
	raise SyntaxError("invalid syntax")
# Build the parser.
parser = yacc.yacc()
result = parser.parse(content)