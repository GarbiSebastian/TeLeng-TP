## p_empty
# def p_reglas_lambda(t):
# 	'reglas :'
# 	pass
# def p_masreglas_lambda(t):
# 	'masreglas :'
# 	pass

## p_operadores_binarios
# def p_numero_mas_factor(t):
# 	"numero : numero '+' factor"
# 	t[0] = t[1] + t[3]
# def p_numero_menos_factor(t):
# 	"numero : numero '-' factor"
# 	t[0] = t[1] - t[3]
# def p_factor_por_termino(t):
# 	"factor : factor '*' termino"
# 	t[0] = t[1] * t[3]
# def p_factor_div_termino(t):
# 	"factor : factor '/' termino"
# 	t[0] = t[1] / t[3]

## p_salteo
# def p_numero_salteo(t):
# 	"numero : factor"
# 	t[0] = t[1]
# def p_factor_salteo(t):
# 	"factor : termino"
# 	t[0] = t[1]
# def p_termino_num(t):
# 	"termino : NUM"
# 	t[0] = t[1]
