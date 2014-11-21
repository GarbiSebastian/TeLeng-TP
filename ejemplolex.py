#Listing Two

"""This file contains the parser rules.

The function yacc.parse, which this function makes available, returns a parse 
tree.  The parse tree is a set of nested lists containing ints, floats, 
strings, Symbols, etc.
"""
import yacc
import sys

from lexer import tokens
from Symbol import Symbol

def p_list(t):
    'list : LPAREN nodes RPAREN'
    t[0] = t[2]
def p_nodes_node(t):
    'nodes : node nodes'
    t[0] = [t[1]] + t[2]
def p_nodes_empty(t):
    'nodes : empty'
    t[0] = []
def p_empty(t):
    'empty :'
    pass
def p_node_int(t):
    'node : INT'
    t[0] = t[1]
def p_node_float(t):
    'node : FLOAT'
    t[0] = t[1]
def p_node_string(t):
    'node : STRING'
    t[0] = t[1]
def p_node_symbol(t):
    'node : SYMBOL'
    t[0] = Symbol(name = t[1])
def p_node_list(t):
    'node : list'
    t[0] = t[1]
# Error rule for syntax errors.
def p_error(t):
    raise SyntaxError("invalid syntax")
# Build the parser.
yacc.yacc()