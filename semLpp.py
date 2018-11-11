from lexLpp import tokens
from sinLpp import tree, r, vars
from ast import Tree, Node
import finder

def checkSiNo(Node):
    pass

def checkPeroSi(node):
    pass

def checkCondicional(node):
    pass

def checkPor(node):
    pass

def checkMientras(node):
    pass

def checkProcedimiento(node):
    obj = node.children[0].value
    #Checks if the PROCEDIMIENTO's name is in the vars dictionary (it should)
    if obj.get('value') not in vars:
        print("ERROR")
        exit(0)

def checkOpArit(node):
    pass

def checkOpRel(node):
    pass

def checkOpLog(node):
    pass

def checkDeclaracion(node):
    decType = node.children[0].value
    id = node.children[1].value
    #check if the var's name is in the vars dictionary (it should)
    if id.get('value') not in vars:
        exit(0)

def checkAsignacion(node):
    pass

def checkInstancia(node):
    varType = node.children[0].value.get('category').split('TIPO_')[1]
    varId = node.children[1].value
    varValue = node.children[2]

    if varId.get('value') not in vars:
        exit(0)

    if type(varValue) is Node:
        if varType != varValue.value.get('category'):
            print(f'ERROR: Variable {varId.get("value")} con valor asignado de tipo de dato incorrecto.')
        exit(0)

def noCheck(node):
    pass

def checkNode(node):
    switch = {
        'Procedimiento': checkProcedimiento,
        'Declaracion': checkDeclaracion,
        'Asignacion': checkAsignacion,
        'Operacion Aritmetica': checkOpArit,
        'Operacion Relacional': checkOpRel,
        'Operacion Logica': checkOpLog,
        'Instancia': checkInstancia,
        'Por': checkPor,
        'Mientras': checkMientras,
        'Condicional': checkCondicional,
        'Pero Si': checkPeroSi,
        'Si No': checkSiNo
    }
    if type(node.value) is not dict:
        func = switch.get(node.value, noCheck)
        func(node)

def analyze(node):
    checkNode(node)
    for child in node.children:
        analyze(child)

print(tree)
analyze(tree.start)