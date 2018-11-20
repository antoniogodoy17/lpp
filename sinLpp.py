import ply.yacc as yacc
from ast import Tree, Node

class SyntacticAnalyzer():
    def __init__(self, tokens):
        self.tree = Tree()
        self.vars = {}
        if tokens:
            self.tokens = tokens
        else:
            exit(0)
        self.build()

    def p_programa(self, p):
        '''programa : sentencias'''
        p[0] = ('Programa',p[1])

    def p_sentencias(self, p):
        '''sentencias : vacio
                    | sentencia sentencias'''
        if len(p) > 2:
            p[0] = ('Sentencias',p[1],p[2])
        else:
            p[0] = ('Sentencias',p[1])

    def p_sentencia(self, p):
        '''sentencia : ciclo
                    | condicional
                    | declaracion
                    | asignacion
                    | instancia
                    | procedimiento'''
        p[0] = ('Sentencia',p[1])

    def p_ciclo(self, p):
        '''ciclo : por
                | mientras'''
        p[0] = ('Ciclo',p[1])

    def p_por(self, p): 
        '''por : POR SIGNO_PAR_IZQ IDENTIFICADOR SIGNO_PAR_DER EN SIGNO_PAR_IZQ termino COMA termino COMA termino SIGNO_PAR_DER SIGNO_LLAVE_IZQ sentencias SIGNO_LLAVE_DER'''
        p[0] = ('Por',p[3],p[7],p[9],p[11],p[14])

    def p_mientras(self, p):
        '''mientras : MIENTRAS SIGNO_PAR_IZQ expresion SIGNO_PAR_DER SIGNO_LLAVE_IZQ sentencias SIGNO_LLAVE_DER'''
        p[0] = ('Mientras',p[3],p[6])

    def p_condicional(self, p):
        '''condicional : SI SIGNO_PAR_IZQ expresion SIGNO_PAR_DER ENTONCES SIGNO_LLAVE_IZQ sentencias SIGNO_LLAVE_DER perosi_op sino_op'''
        p[0] = ('Condicional',p[3],p[7],p[9],p[10])

    def p_perosi_op(self, p):
        '''perosi_op : vacio 
                    | PEROSI SIGNO_PAR_IZQ expresion SIGNO_PAR_DER ENTONCES SIGNO_LLAVE_IZQ sentencias SIGNO_LLAVE_DER perosi_op'''
        if len(p) > 2:
            p[0] = ('Pero Si', p[3],p[7],p[9])
        else:
            p[0] = ('Pero Si', p[1])

    def p_sino_op(self, p):
        '''sino_op : vacio
                | SINO SIGNO_LLAVE_IZQ sentencias SIGNO_LLAVE_DER'''
        if len(p) > 2:
            p[0] = ('Si No',p[3])
        else:
            p[0] = ('Si No',p[1])

    def p_declaracion(self, p):
        '''declaracion : tipo IDENTIFICADOR TERMINACION'''
        p[0] = ('Declaracion',p[1],p[2])
        if p[2].get('value') in self.vars:
            self.vars.pop(p[2].get('value'))
        self.vars[p[2].get('value')] = { 'category' : p[1].get('value'), 'value' : 'NULO'}

    def p_asignacion(self, p):
        '''asignacion : IDENTIFICADOR ASIGNACION valor TERMINACION'''
        p[0] = ('Asignacion',p[1], p[3])
        if p[1].get('value') in self.vars:
            varType = self.vars[p[1].get('value')].get('category')
            varValue = self.vars[p[1].get('value')].get('value')
            self.vars.pop(p[1].get('value'))
            if type(p[3]) is tuple and type(p[3]) is tuple:
                if p[3][1].get('value') == p[1].get('value'):
                    #Change the value of the p[0] tuple
                    parentList = list(p[0])
                    childList = list(parentList[2])
                    childList[1] = { 'category': varType,'value': varValue }
                    parentList[2] = tuple(childList)
                    p[0] = tuple(parentList)

                    #Change the value of the p[3] tuple
                    parentList = list(p[3])
                    childList = list(parentList[1])
                    childList = { 'category': varType,'value': varValue }
                    # print(childList)
                    parentList[1] = childList
                    # print(parentList)
                    p[3] = tuple(parentList)
                self.vars[p[1].get('value')] = { 'category' : varType, 'value' : (p[3][0],p[3][1],p[3][2],p[3][3])}
            elif type(p[3]) is dict:
                self.vars[p[1].get('value')] = { 'category' : varType, 'value' : p[3].get('value')}

    def p_instancia(self, p):
        '''instancia : tipo IDENTIFICADOR ASIGNACION valor TERMINACION'''
        p[0] = ('Instancia',p[1],p[2],p[4])
        if p[2].get('value') in self.vars:
            if type(p[4]) is tuple and p[4][1].get('value') == p[1].get('value'):
                #Change the value of the p[0] tuple
                parentList = list(p[0])
                childList = list(parentList[2])
                childList[1] = { 'category': varType,'value': varValue }
                parentList[2] = tuple(childList)
                p[0] = tuple(parentList)

                #Change the value of the p[4] tuple
                parentList = list(p[4])
                childList = list(parentList[1])
                childList = { 'category': varType,'value': varValue }
                # print(childList)
                parentList[1] = childList
                # print(parentList)
                p[4] = tuple(parentList)
            self.vars.pop(p[2].get('value'))
        if type(p[4]) is tuple:
            self.vars[p[2].get('value')] = { 'category' : p[1].get('value'), 'value' : (p[4][0],p[4][1],p[4][2],p[4][3])}
        elif type(p[4]) is dict:
            self.vars[p[2].get('value')] = { 'category' : p[1].get('value'), 'value' : p[4].get('value')}

    def p_valor(self, p):
        '''valor : BOOLEANO
                | numero
                | CADENA
                | IDENTIFICADOR 
                | expresion'''
        p[0] = p[1]

    def p_expresion(self, p):
        '''expresion : operacion_aritmetica
                    | operacion_logica
                    | operacion_relacional'''
        p[0] = p[1]

    def p_termino(self, p):
        '''termino : numero
                | IDENTIFICADOR
                | SIGNO_PAR_IZQ operacion_aritmetica SIGNO_PAR_DER'''
        if len(p) > 2:
            p[0] = p[2]
        else:
            p[0] = p[1]

    def p_operacion_aritmetica(self, p):
        '''operacion_aritmetica : termino operador_aritmetico termino'''
        p[0] = ('Operacion Aritmetica', p[1],p[2],p[3])

    def p_operacion_relacional(self, p):
        '''operacion_relacional : valor operador_relacional valor'''
        p[0] = ('Operacion Relacional',p[1],p[2],p[3])

    def p_operacion_logica(self, p):
        '''operacion_logica : SIGNO_PAR_IZQ expresion SIGNO_PAR_DER operador_logico SIGNO_PAR_IZQ expresion SIGNO_PAR_DER
                            | SIGNO_PAR_IZQ termino SIGNO_PAR_DER operador_logico SIGNO_PAR_IZQ termino SIGNO_PAR_DER'''
        p[0] = ('Operacion Logica',p[2],p[4],p[6])

    def p_procedimiento(self, p):
        '''procedimiento : PROCEDIMIENTO IDENTIFICADOR SIGNO_PAR_IZQ parametros_op SIGNO_PAR_DER SIGNO_LLAVE_IZQ sentencias regresa_op SIGNO_LLAVE_DER'''
        p[0] = ('Procedimiento', p[2],p[4],p[7],p[8])
        self.vars[p[2].get('value')] = { 'category': p[1].get('value'), 'value': p[2].get('value') }

    def p_parametros_op(self, p):
        '''parametros_op : vacio
                        | parametros_op COMA parametro
                        | parametro'''
        if len(p) > 2:
            p[0] = ('Parametros Opcionales',p[1],p[3])
        else:
            p[0] = ('Parametros Opcionales', p[1])

    def p_parametro(self, p):
        '''parametro : termino
                    | CADENA
                    | BOOLEANO'''
        p[0] = ('Parametro', p[1])
                    
    def p_regresa_op(self, p):
        '''regresa_op : vacio
                    | REGRESA valor TERMINACION'''
        if len(p) > 2:
            p[0] = ('Regresa Opcional', p[2])
        else:
            p[0] = ('Regresa Opcional', p[1])

    def p_numero(self, p):
        '''numero : ENTERO
                | DECIMAL'''
        p[0] = p[1]

    def p_tipo(self, p):
        '''tipo : TIPO_ENTERO
                | TIPO_DECIMAL
                | TIPO_BOOLEANO
                | TIPO_CADENA
                | TIPO_CONSTANTE'''
        p[0] = p[1]

    def p_operador_aritmetico(self, p):
        '''operador_aritmetico : SIGNO_MULT
                            | SIGNO_SUM
                            | SIGNO_RES
                            | SIGNO_DIV
                            | SIGNO_MOD'''
        p[0] = p[1]

    def p_operador_logico(self, p):
        '''operador_logico : SIGNO_O
                        | SIGNO_Y'''
        p[0] = p[1]

    def p_operador_relacional(self, p):
        '''operador_relacional : MAYOR_IGUAL
                            | MENOR_IGUAL
                            | DIFERENTE
                            | IGUAL
                            | MAYOR
                            | MENOR'''
        p[0] = p[1]

    def p_vacio(self, p):
        '''vacio :'''
        pass

    def p_error(self, p):
        print(f'Error de sintaxis en la linea {str(p.lineno)}. "{p}"')

    def printNodes(self, l, level=0):
        sentType = l[0]
        children = l[1:] 
        tabs = "--" * level

        print(f'[{level}]{tabs}{sentType}:')
        for elem in children:
            if type(elem) is tuple:
                printNodes(elem, level+1)
            else:
                print(f'[{level}]{tabs + "--"}{elem}')

    def createTree(self, l=[], level=0, parent=None):
        sentType = l[0]
        children = l[1:]
        node = Node(value=sentType, level=level)
        
        if parent:
            parent.addChild(node)

        if level == 0:
            self.tree.setStart(node)

        for elem in children:
            if type(elem) is tuple:
                self.createTree(l=elem, level=level+1, parent=node)
            else:
                child = Node(level=level+1,value=elem)
                node.addChild(child)

    def build(self):
        self.parser = yacc.yacc(module=self)

    def analyze(self, data):
        self.output = self.parser.parse(data)
        self.createTree(self.output)