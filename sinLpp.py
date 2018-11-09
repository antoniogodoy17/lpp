import ply.yacc as yacc
from lexLpp import tokens
import finder

start = 'programa'

def p_programa(p):
    '''programa : sentencias'''
    p[0] = ('Programa',p[1])

def p_sentencias(p):
    '''sentencias : vacio
                  | sentencia sentencias'''
    if len(p) > 2:
        p[0] = ('Sentencias',p[1],p[2])
    else:
        p[0] = ('Sentencias',p[1])

def p_sentencia(p):
    '''sentencia : ciclo
                 | condicional
                 | declaracion
                 | asignacion
                 | instancia
                 | procedimiento'''
    p[0] = ('Sentencia',p[1])

def p_ciclo(p):
    '''ciclo : por
             | mientras'''
    p[0] = ('Ciclo',p[1])

def p_por(p): 
    '''por : POR SIGNO_PAR_IZQ IDENTIFICADOR SIGNO_PAR_DER EN SIGNO_PAR_IZQ termino COMA termino COMA termino SIGNO_PAR_DER SIGNO_LLAVE_IZQ sentencias SIGNO_LLAVE_DER'''
    p[0] = ('Por',p[3],p[7],[9],p[11],p[14])

def p_mientras(p):
    '''mientras : MIENTRAS SIGNO_PAR_IZQ expresion SIGNO_PAR_DER SIGNO_LLAVE_IZQ sentencias SIGNO_LLAVE_DER'''
    p[0] = ('Mientras',p[3],p[6])

def p_condicional(p):
    '''condicional : SI SIGNO_PAR_IZQ expresion SIGNO_PAR_DER ENTONCES SIGNO_LLAVE_IZQ sentencias SIGNO_LLAVE_DER perosi_op sino_op'''
    p[0] = ('Condicional',p[3],p[7],p[9],p[10])

def p_perosi_op(p):
    '''perosi_op : vacio 
                 | PEROSI SIGNO_PAR_IZQ expresion SIGNO_PAR_DER ENTONCES SIGNO_LLAVE_IZQ sentencias SIGNO_LLAVE_DER perosi_op'''
    if len(p) > 2:
        p[0] = ('Pero Si Opcional', p[3],p[7],p[9])
    else:
        p[0] = ('Pero Si Opcional', p[1])

def p_sino_op(p):
    '''sino_op : vacio
               | SINO SIGNO_LLAVE_IZQ sentencias SIGNO_LLAVE_DER'''
    if len(p) > 2:
        p[0] = ('Si No Opcional',p[3])
    else:
        p[0] = ('Si No Opcional',p[1])

def p_declaracion(p):
    '''declaracion : tipo IDENTIFICADOR TERMINACION'''
    p[0] = ('Declaracion',p[1],p[2])

def p_asignacion(p):
    '''asignacion : IDENTIFICADOR ASIGNACION valor TERMINACION'''
    p[0] = ('Asignacion',p[1], p[3])

def p_instancia(p):
    '''instancia : tipo IDENTIFICADOR ASIGNACION valor TERMINACION'''
    p[0] = ('Instancia',p[1],p[2],p[4])

def p_valor(p):
    '''valor : BOOLEANO
             | numero
             | CADENA
             | IDENTIFICADOR 
             | expresion
             | NULO'''
    p[0] = ('Valor',p[1])

def p_expresion(p):
    '''expresion : operacion_aritmetica
                 | operacion_logica
                 | operacion_relacional'''
    p[0] = ('Expresion',p[1])

def p_termino(p):
    '''termino : numero
               | IDENTIFICADOR
               | SIGNO_PAR_IZQ operacion_aritmetica SIGNO_PAR_DER'''
    if len(p) > 2:
        p[0] = ('Termino',p[2])
    else:
        p[0] = ('Termino',p[1])

def p_operacion_aritmetica(p):
    '''operacion_aritmetica : termino operador_aritmetico termino'''
    p[0] = ('Operacion Aritmetica', p[1],p[2],p[3])

def p_operacion_relacional(p):
    '''operacion_relacional : valor operador_relacional valor'''
    p[0] = ('Operacion Relacional',p[1],p[2],p[3])

def p_operacion_logica(p):
    '''operacion_logica : SIGNO_PAR_IZQ expresion SIGNO_PAR_DER operador_logico SIGNO_PAR_IZQ expresion SIGNO_PAR_DER
                        | SIGNO_PAR_IZQ termino SIGNO_PAR_DER operador_logico SIGNO_PAR_IZQ termino SIGNO_PAR_DER'''
    p[0] = ('Operacion Logica',p[2],p[4],p[6])

def p_procedimiento(p):
    '''procedimiento : PROCEDIMIENTO IDENTIFICADOR SIGNO_PAR_IZQ parametros_op SIGNO_PAR_DER SIGNO_LLAVE_IZQ sentencias regresa_op SIGNO_LLAVE_DER'''
    p[0] = ('Procedimiento', p[2],p[4],p[7],p[8])

def p_parametros_op(p):
    '''parametros_op : vacio
                     | parametros_op COMA parametro
                     | parametro'''
    if len(p) > 2:
        p[0] = ('Parametros Opcionales',p[1],p[3])
    else:
        p[0] = ('Parametros Opcionales', p[1])

def p_parametro(p):
    '''parametro : termino
                 | CADENA
                 | BOOLEANO'''
    p[0] = ('Parametro', p[1])
                
def p_regresa_op(p):
    '''regresa_op : vacio
                  | REGRESA valor TERMINACION'''
    if len(p) > 2:
        p[0] = ('Regresa Opcional', p[2])
    else:
        p[0] = ('Regresa Opcional', p[1])

def p_numero(p):
    '''numero : ENTERO
              | DECIMAL'''
    p[0] = ('Numero', p[1])

def p_tipo(p):
    '''tipo : TIPO_ENTERO
            | TIPO_DECIMAL
            | TIPO_BOOLEANO
            | TIPO_CADENA
            | TIPO_CONSTANTE'''
    p[0] = ('Tipo',p[1])

def p_operador_aritmetico(p):
    '''operador_aritmetico : SIGNO_MULT
                           | SIGNO_SUM
                           | SIGNO_RES
                           | SIGNO_DIV
                           | SIGNO_MOD'''
    p[0] = ('Operador Aritmetico', p[1])

def p_operador_logico(p):
    '''operador_logico : SIGNO_O
                       | SIGNO_Y'''
    p[0] = ('Operador Logico', p[1])

def p_operador_relacional(p):
    '''operador_relacional : MAYOR_IGUAL
                           | MENOR_IGUAL
                           | DIFERENTE
                           | IGUAL
                           | MAYOR
                           | MENOR'''
    p[0] = ('Operador Relacional', p[1])

def p_vacio(p):
    '''vacio :'''
    pass

def p_error(p):
	print(f'Error de sintaxis en la linea {str(p.lineno)}.\n\t"{p}"')

def printNodes(l, level=0):
    sentType = l[0]
    children = l[1:] 
    tabs = ""

    for i in range(level):
        tabs += "--"

    print(f'[{level}]{tabs}{sentType}:')
    for elem in children:
        if type(elem) is tuple:
            printNodes(elem, level+1)
        else:
            tempTabs = tabs + "--"
            print(f'[{level+1}]{tabs + "--"}{elem}')

parser = yacc.yacc()
r = parser.parse(finder.search())
printNodes(r)

