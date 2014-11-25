# -----------------------------------------------------------------------------
# module: lexer.py
# Lexer Rules
# -----------------------------------------------------------------------------
import ply.lex as lex
import sys
import re

literals = ['.',':','|','&','[',']','<','>','^','=','$','+','-','*','/','(',')']

#reservadas
reserved = {
	"ball" : "BALL",
	"box"  : "BOX",
	"_"    : "NADA",
	'rx'   : "RX",
	'ry'   : "RY",
	'rz'   : "RZ",
	'sx'   : "SX",
	'sy'   : "SY",
	'sz'   : "SZ",
	's'    : "S",
	'tx'   : "TX",
	'ty'   : "TY",
	'tz'   : "TZ",
	'cr'   : "CR",
	'cg'   : "CG",
	'cb'   : "CB",
	'd'    : "D"
}

#Token names
tokens = [
	'NUM',
	'REGLA'
]+list(reserved.values())

t_NADA = r'_'

def t_comment(t):
	r'".*"'
	pass

def t_REGLA(t):
	r'[a-zA-Z]+'
	t.type = reserved.get(t.value,'REGLA')    # Check for reserved words
	return t

def t_NUM(t):
	r'\d+(\.\d+)?'
	try:
		t.value = float(t.value)
	except ValueError:
		print "Pasame un numerito de verdad", t.value
		t.value = 0
	return t

t_ignore = ' \t\n\r'

# Track line numbers.
def t_newline(t):
	r'((\r\n)+|\n+|\r+)'
	t.lineno += len(t.value)

def t_error(t):
	raise SyntaxError("syntax error on line %d near '%s'" %(t.lineno, t.value))
	print "error"
# Build the lexer.
lexer = lex.lex()