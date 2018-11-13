from lexLpp import tokens
from sinLpp import tree, r, vars
from ast import Tree, Node
import finder

def throwError(message):
    print(message)
    print(vars)
    exit(0)

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
        throwError(f'ERROR: Procedimiento {obj.get("value")} no existe.')

def checkOpArit(node):
    left = node.children[0]
    op = node.children[1].value.get('value')
    right = node.children[2]

    #Check if the left value is an aritmetic operation
    if left.value == 'Operacion Aritmetica':
        left = checkOpArit(node.children[0])
    #Check if the left value is a dictionary,then it could be an identifier so we need to extract its value and assign it to left
    elif type(left.value) is dict:
        if left.value.get('category') == 'IDENTIFICADOR':
            #If left is a var, get the var value from the vars dictionary
            if left.value.get('value') in vars:
                left = vars[left.value.get('value')]
            #If left is a var and it is not in the vars dictionary, throw an error
            else:
                throwError(f'ERROR: Variable {left.value.get("value")} no declarada.')
        else:
            #If left is a dictionary but not an identifier, just extract its value
            left = left.value

    #Check if the right value is an aritmetic operation
    if right.value == 'Operacion Aritmetica':
        right = checkOpArit(node.children[2])
    #Check if the right value is a dictionary,then it could be an identifier so we need to extract its value and assign it to left
    elif type(right.value) is dict:
        if right.value.get('category') == 'IDENTIFICADOR':
            #If right is a var, get the var value from the vars dictionary
            if right.value.get('value') in vars:
                right = vars[right.value.get('value')]
            #If right is a var and it is not in the vars dictionary, throw an error
            else:
                throwError(f'ERROR: Variable {right.value.get("value")} no declarada.')
        else:
            #If right is a dictionary but not an identifier, just extract its value 
            right = right.value

    #Check value
    if left.get('value') == 'NULO' or right.get('value') == 'NULO':
        throwError(f'ERROR: Valores incompatibles para realizar operacion. {left.get("value")} y {right.get("value")}')
    
    if op == '+':
        if left.get('category') == right.get('category'):
            result = { 'category': left.get('category'), 'value': left.get('value') + right.get('value') }
        else:
            throwError(f'ERROR: No se pudo ejecutar la operación con valores incompatibles {left.get("category")} y {right.get("category")}.')

    if op == '-':
        if left.get('category') == right.get('category'):
            result = { 'category': left.get('category'), 'value': left.get('value') - right.get('value') }
        else:
            throwError(f'ERROR: No se pudo ejecutar la operación con valores incompatibles {left.get("category")} y {right.get("category")}.')
        
    if op == '*':
        if left.get('category') == right.get('category'):
            result = { 'category': left.get('category'), 'value': left.get('value') * right.get('value') }
        else:
            throwError(f'ERROR: No se pudo ejecutar la operación con valores incompatibles {left.get("category")} y {right.get("category")}.')

    if op == '/':
        if left.get('category') == right.get('category') and left.get('category') == 'ENTERO':
            result = { 'category': left.get('category'), 'value': left.get('value') // right.get('value') }
        elif left.get('category') == right.get('category') and left.get('category') == 'DECIMAL':
            result = { 'category': left.get('category'), 'value': left.get('value') / right.get('value') }
        else:
            throwError(f'ERROR: No se pudo ejecutar la operación con valores incompatibles {left.get("category")} y {right.get("category")}.')

    return result

def checkOpRel(node):
    left = node.children[0]
    op = node.children[1].value.get('value')
    right = node.children[2]

    #Check left

    #Check right

    #Check value
    if op == '=':
        pass
    if op == '<':
        pass
    if op == '>':
        pass
    if op == '<=':
        pass
    if op == '>=':
        pass
    if op == '?':
        pass

def checkOpLog(node):
    left = node.children[0]
    op = node.children[1].value.get('value')
    right = node.children[2]

    # print("***************************")
    # print(left.children)
    # print(right.value)
    # print("***************************")

    #Check left
    if left.value == 'Operacion Aritmetica':
        left = checkOpArit(left)
    # elif left.value == 'Operacion Ar'

    #Check right

    #Check value
    if op == '&':
        pass
    if op == '|':
        pass

def checkDeclaracion(node):
    varId = node.children[1].value.get('value')
    #Check if the var exists in the vars dictionary
    if varId not in vars:
        throwError(f'ERROR: Variable {varId} no declarada.')

def checkAsignacion(node):
    varId = node.children[0].value.get('value')
    newValue = node.children[1].value
    #Check if the var exists in the vars dictionary
    if varId in vars:
        #Extract its type
        varType = vars[varId].get('category')
        
        #Check if value is an aritmetic operation
        if newValue == 'Operacion Aritmetica':
            newValue = checkOpArit(node.children[1])
            vars.pop(varId)
            vars[varId] = newValue
        #Check if value is an identifier
        elif newValue.get('category') == 'IDENTIFICADOR':
            #Check if var exists in vars dictionary
            if newValue.get('value') in vars:
                newValue = vars[newValue.get('value')]
                
                #Check if value type is equal to var type
                if varType == newValue.get('category'):
                    vars.pop(varId)
                    vars[varId] = newValue
                else:
                    throwError(f'ERROR: {newValue.get("value")} es de tipo diferente a {varId}')
            #Throw error
            else:
                throwError(f'ERROR: Variable {newValue.get("value")} no declarada.')
        #Check if value is NULO
        elif newValue.get('category') == 'NULO':
            pass
        #Value should be some other value
        else:
            if varType == newValue.get('category'):
                vars.pop(varId)
                vars[varId] = newValue
            else:
                throwError(f'ERROR: {newValue.get("value")} es de tipo diferente a {varId}.')
    #If not in the vars dictionary, throw error
    else:
        throwError(f'ERROR: Variable {varId} no declarada.')

def checkInstancia(node):
    varType = node.children[0].value.get('category').split('TIPO_')[1]
    varId = node.children[1].value.get('value')
    varValue = node.children[2]
    newValue = 0

    #Check if variable is already in the vars dict
    if varId not in vars:
        throwError(f'ERROR: Variable {varId} no declarada.')
            
    #Check if the variable value and the variable type are the same
    if type(varValue.value) is dict:
        #If the type is different from the var type, throw error
        if varType != varValue.value.get('category'):
            throwError(f'ERROR: Variable {varId.get("value")} con valor asignado de tipo de dato incorrecto.')
    elif varValue.value == 'Operacion Aritmetica':
        #Check aritmetic operation
        newValue = checkOpArit(varValue)
        #Delete variable with old value from dictionary
        vars.pop(varId)
        #Add the key with the new assigned value
        vars[varId] = newValue

        print(f'LEFT: {left}')
def noCheck(node):
    pass

def checkNode(node):
    switch = {
        'Operacion Aritmetica': checkOpArit,
        'Operacion Relacional': checkOpRel,
        'Operacion Logica': checkOpLog,
        'Procedimiento': checkProcedimiento,
        'Declaracion': checkDeclaracion,
        'Asignacion': checkAsignacion,
        'Instancia': checkInstancia,
        'Condicional': checkCondicional,
        'Mientras': checkMientras,
        'Pero Si': checkPeroSi,
        'Si No': checkSiNo,
        'Por': checkPor
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
print(vars)