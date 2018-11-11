import ply.lex as lex
import finder

operadores = {
    '*' : 'SIGNO_MULT',
    '+' : 'SIGNO_SUM',
    '-' : 'SIGNO_RES',
    '/' : 'SIGNO_DIV',
    '%' : 'SIGNO_MOD',

    '>=': 'MAYOR_IGUAL',
    '<=': 'MENOR_IGUAL',
    '?' : 'DIFERENTE',
    '=' : 'IGUAL',
    '>' : 'MAYOR',
    '<' : 'MENOR',

    '|' : 'SIGNO_O',
    '&' : 'SIGNO_Y',

    '{' : 'SIGNO_LLAVE_IZQ',
    '}' : 'SIGNO_LLAVE_DER',
    '(' : 'SIGNO_PAR_IZQ',
    ')' : 'SIGNO_PAR_DER',

    ';' : 'TERMINACION',
    ':' : 'DOS_PUNTOS',
    '.' : 'PUNTO',
    ',' : 'COMA'
}

categorias = {
    'SIGNO_MULT'        : 'OPERADORES_ARITMETICOS',
    'SIGNO_SUM'         : 'OPERADORES_ARITMETICOS',
    'SIGNO_RES'         : 'OPERADORES_ARITMETICOS',
    'SIGNO_DIV'         : 'OPERADORES_ARITMETICOS',
    'SIGNO_MOD'         : 'OPERADORES_ARITMETICOS',

    'MAYOR_IGUAL'       : 'OPERADORES_RELACIONALES',
    'MENOR_IGUAL'       : 'OPERADORES_RELACIONALES',
    'DIFERENTE'         : 'OPERADORES_RELACIONALES',
    'IGUAL'             : 'OPERADORES_RELACIONALES',
    'MAYOR'             : 'OPERADORES_RELACIONALES',
    'MENOR'             : 'OPERADORES_RELACIONALES',

    'SIGNO_O'           : 'OPERADORES_LOGICOS',
    'SIGNO_Y'           : 'OPERADORES_LOGICOS',

    'SIGNO_LLAVE_IZQ'   : 'AGRUPACION',
    'SIGNO_LLAVE_DER'   : 'AGRUPACION',
    'SIGNO_PAR_IZQ'     : 'AGRUPACION',
    'SIGNO_PAR_DER'     : 'AGRUPACION',

    'TERMINACION'       : 'PUNTUACION',
    'DOS_PUNTOS'        : 'PUNTUACION',
    'PUNTO'             : 'PUNTUACION',
    'COMA'              : 'PUNTUACION',

    'TIPO_BOOLEANO'     : 'TIPO',
    'TIPO_DECIMAL'      : 'TIPO',
    'TIPO_CADENA'       : 'TIPO',
    'TIPO_ENTERO'       : 'TIPO',
    'TIPO_CONSTANTE'    : 'TIPO',
    'NULO'              : 'NULO',

    'PROCEDIMIENTO'     : 'RESERVADA',
    'ENTONCES'          : 'RESERVADA',
    'MIENTRAS'          : 'RESERVADA',
    'PEROSI'            : 'RESERVADA',
    'REGRESA'           : 'RESERVADA',
    'SINO'              : 'RESERVADA',
    'POR'               : 'RESERVADA',
    'FIN'               : 'RESERVADA',
    'SI'                : 'RESERVADA',
    'EN'                : 'RESERVADA',

    'VERDADERO'         : 'BOOLEANO',
    'FALSO'             : 'BOOLEANO'
}

tok_reservadas = ['SI','ENTONCES', 'PEROSI', 'SINO', 'MIENTRAS', 'POR', 'EN', 'PROCEDIMIENTO', 'REGRESA', 'FIN']
tok_tipos = ['ENTERO', 'DECIMAL', 'CADENA', 'BOOLEANO','CONSTANTE']

tokens = ['ASIGNACION', 'COMENTARIO', 'BOOLEANO', 'IDENTIFICADOR', 'DECIMAL', 'ENTERO', 'CADENA', 'OPERADOR_RELACIONAL', 'OPERADOR_ARITMETICO', 'OPERADOR_LOGICO', 'SIGNOS_PUNTUACION', 'SIGNOS_AGRUPACION', 'TIPO'] +  list(categorias.keys())

#Caracteres a ignorar (Solo el espacio, por ahora)
t_ignore = r' '

def t_error(t):
    print(f'ERROR: Caracter Ilegal "{t.value[0]}".')
    t.lexer.skip(1)

def t_NEWLINE(t):
    r'[\r\n]+'
    t.lexer.lineno += len(t.value)

def t_ASIGNACION(t):
    r'->'
    t.value = {
        'category' : 'ASIGNACION',
        'value' : t.value
    }
    return t

def t_COMENTARIO(t):
    r'@(.|\n)*@'
    pass

def t_BOOLEANO(t):
    r'(VERDADERO|FALSO)'
    t.value = {
        'category' : categorias.get(t.value,t.type),
        'value' : t.value
    }
    return t

def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value in tok_tipos:
        t.type = "TIPO_" + t.value
    if t.value in tok_reservadas:
        t.type = t.value
    t.value = {
        'category' : categorias.get(t.value, t.type),
        'value' : t.value
    }
    return t
    
def t_DECIMAL(t):
    r'-?\d+\.\d+'
    t.value = {
        'category' : 'DECIMAL',
        'value' : float(t.value)
    }
    # t.value = float(t.value)
    return t

def t_ENTERO(t):
    r'-?\d+'
    t.value = {
        'category' : 'ENTERO',
        'value' : int(t.value)
    }
    # t.value = int(t.value)
    return t

def t_CADENA(t):
    r'".*"'
    t.value = {
        'category' : t.type,
        'value' : t.value
    }
    return t

def t_OPERADOR_RELACIONAL(t):
    r'>= | <= | = | \? | > | <'
    t.type = operadores.get(t.value, t.type)
    t.value = {
        'category' : categorias.get(t.type, t.type),
        'value' : t.value
    }
    return t

def t_OPERADOR_ARITMETICO(t):
    r'\+ | \* | - | \/ | %'
    t.type = operadores.get(t.value, t.type)
    t.value = {
        'category' : categorias.get(t.type,t.type),
        'value' : t.value
    }
    return t

def t_OPERADOR_LOGICO(t):
    r'\| | &'
    t.type = operadores.get(t.value, t.type)
    t.value = {
        'category' : categorias.get(t.type, t.type),
        'value' : t.value
    }
    return t

def t_SIGNOS_PUNTUACION(t):
    r', | : | ; | \.'
    t.type = operadores.get(t.value, t.type)
    t.value = {
        'category' : categorias.get(t.type, t.type),
        'value' : t.value
    }
    return t  

def t_SIGNOS_AGRUPACION(t):
    r'\( | \) | \{ | \}'
    t.type = operadores.get(t.value, t.type)
    t.value = {
        'category' : categorias.get(t.type, t.type),
        'value' : t.value
    }
    return t  

analizador = lex.lex()
# analizador.input(archivero.buscar())

# for token in analizador:
#     print(token)