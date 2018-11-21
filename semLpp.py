from ast import Tree, Node

class SemanticAnalyzer():
    def __init__(self):
        self.variables = {}
        self.tempVars = 0
        self.scopes = 0
        self.labels = []

    def analyze(self, node):
        self.checkNode(node)

    def checkNode(self, node):
        switch = {
            'Programa': self.checkPrograma,
            'Sentencia': self.checkSentencia,
            'Sentencias': self.checkSentencias,
            'Operacion Aritmetica': self.checkOpArit,
            'Operacion Relacional': self.checkOpRel,
            'Operacion Logica': self.checkOpLog,
            'Procedimiento': self.checkProcedimiento,
            'Declaracion': self.checkDeclaracion,
            'Asignacion': self.checkAsignacion,
            'Instancia': self.checkInstancia,
            'Condicional': self.checkCondicional,
            'Mientras': self.checkMientras,
            'Pero Si': self.checkPeroSi,
            'Ciclo': self.checkCiclo,
            'Si No': self.checkSiNo,
            'Por': self.checkPor
        }
        if type(node.value) is not dict:
            func = switch.get(node.value, self.noCheck)
            func(node=node)

    def noCheck(self, node):
        pass

    def throwError(self, message):
        for label in self.labels:
            print(label)
        print(self.variables)
        print(message)
        exit(0)

    def checkPrograma(self, node):
        self.checkNode(node.children[0])

    def checkSentencias(self, node):
        self.checkNode(node.children[0])
        if len(node.children) > 1:
            for child in node.children[1].children:
                self.checkNode(child)

    def checkSentencia(self, node):
        self.checkNode(node.children[0])

    def checkCiclo(self, node):
        self.checkNode(node.children[0])

    def checkDeclaracion(self, node):
        varType = node.children[0].value.get('value')
        varId = node.children[1].value.get('value')
        #Check if the var exists in the self.variables dictionary
        if varId not in self.variables:
            self.variables[varId] = { 'category' : varType, 'value' : 'NULO'}
            self.labels.append( ('->','NULO','',f'T{self.tempVars}') )
            self.labels.append( ('->',varId,f'T{self.tempVars}','') )
            self.tempVars+=1
        else:
            self.throwError(f'ERROR: Variable {varId} no declarada.')

    def checkAsignacion(self, node):
        varId = node.children[0].value.get('value')
        varValue = node.children[1]
        #Check if the var exists in the self.variables dictionary
        if varId in self.variables:
            #Extract its type
            varType = self.variables[varId].get('category')
            
            #Check if value is an aritmetic operation
            if varValue.value == 'Operacion Aritmetica':
                varValue = self.checkOpArit(varValue)
            #Check if value is an identifier
            elif varValue.value == 'Operacion Relacional':
                varValue = self.checkOpRel(varValue)
            elif varValue.value == 'Operacion Logica':
                varValue = self.checkOpLog(varValue)
            elif varValue.value.get('category') == 'IDENTIFICADOR':
                #Check if var exists in self.variables dictionary
                if varValue.value.get('value') in self.variables:
                    varValue = self.variables[varValue.value.get('value')]
                    
                    #Check if value type is equal to var type
                    if varType == varValue.value.get('category'):
                        self.variables.pop(varId)
                        self.variables[varId] = varValue.value
                    else:
                        self.throwError(f'ERROR: {varValue.value.get("value")} es de tipo diferente a {varId}')
                #Throw error
                else:
                    self.throwError(f'ERROR: Variable {varValue.value.get("value")} no declarada.')
            #Check if value is NULO
            elif varValue.value.get('category') == 'NULO':
                varValue = varValue.value
            #Value should be some other value
            else:
                if varType == varValue.value.get('category'):
                    varValue = varValue.value
                else:
                    self.throwError(f'ERROR: {varValue.value.get("value")} es de tipo diferente a {varId}.')
            
            self.variables.pop(varId)
            self.variables[varId] = varValue
            self.labels.append( ('->',varValue.get('value'),'',f'T{self.tempVars}') )
            self.labels.append( ('->',varId,f'T{self.tempVars}','') )
            self.tempVars+=1
        #If not in the self.variables dictionary, throw error
        else:
            self.throwError(f'ERROR: Variable {varId} no declarada.')

    def checkInstancia(self, node):
        varType = node.children[0].value.get('category').split('TIPO_')[1]
        varId = node.children[1].value.get('value')
        varValue = node.children[2]

        #Check if variable is already in the self.variables dict
        if varId in self.variables:
            self.throwError(f'ERROR: La variable "{varId}" ya se encuentra declarada.')
        else:
            if type(varValue.value) is dict:
                varValue = varValue.value
            elif varValue.value == 'Operacion Aritmetica':
                varValue = self.checkOpArit(varValue)
            elif varValue.value == 'Operacion Relacional':
                varValue = self.checkOpRel(varValue)
            elif varValue.value == 'Operacion Logica':
                varValue = self.checkOpLog(varValue)

            if varType == varValue.get('category'):
                self.variables[varId] = { 'category': varType, 'value': varValue.get('value')}
                self.labels.append( ('->',varValue.get('value'),'',f'T{self.tempVars}') )
                self.labels.append( ('->',varId,f'T{self.tempVars}','') )
                self.tempVars+=1
            else:
                self.throwError(f'ERROR: Tipos incompatibles para asignación. {varType} {varId} ? {varValue.get("category")} {varValue.get("value")}')

    def checkProcedimiento(self, node):
        procName = node.children[0].value.get('value')
        myScope = self.scopes
        #Checks if the PROCEDIMIENTO's name is in the self.variables dictionary (it should)
        if procName not in self.variables:
            self.variables[procName] = {'category': 'PROCEDIMIENTO', 'value': procName}
            self.labels.append( (f'L{myScope}','PROCEDIMIENTO') )
            self.scopes+=1
            self.labels.append( ('->','PROCEDIMIENTO','',f'T{self.tempVars}') )
            self.labels.append( ('->',procName,f'T{self.tempVars}','') )
            self.tempVars+=1
        else:
            self.throwError(f'ERROR: Procedimiento {procName} no existe.')

        self.checkNode(node.children[2])
        self.labels.append( (f'L{myScope}','PROCEDIMIENTO') )

    def checkCondicional(self, node):
        myScope = self.scopes
        expr = node.children[0]
        sent = node.children[1]
        peroSi = node.children[2]
        siNo = node.children[3]

        self.labels.append( (f'L{myScope}','CONDICIONAL') )
        self.scopes+=1

        self.checkNode(expr)
        for child in sent.children:
            self.checkNode(child)
        self.checkNode(peroSi)
        self.checkNode(siNo)

        self.labels.append( (f'L{myScope}','CONDICIONAL') )

    def checkPeroSi(self, node):
        myScope = self.scopes

        if len(node.children) > 1:
            self.labels.append( (f'L{myScope}','PERO SI') )
            self.scopes+=1
            expr = node.children[0]
            sent = node.children[1]
            peroSi = node.children[2]

            self.checkNode(expr)
            for child in sent.children:
                self.checkNode(child)
            self.checkNode(peroSi)

            self.labels.append( (f'L{myScope}','PERO SI') )
    
    def checkSiNo(self, node):
        myScope = self.scopes
        sent = node.children[0]

        if len(sent.children) > 0:    
            self.labels.append( (f'L{myScope}','SI NO') )
            self.scopes+=1

            for child in sent.children:
                self.checkNode(child)

            self.labels.append( (f'L{myScope}','SI NO') )

    def checkPor(self, node):
        myScope = self.scopes
        sent = node.children[4]
        self.labels.append( (f'L{myScope}','POR') )
        self.scopes+=1

        for child in sent.children:
            self.checkNode(child)
        
        self.labels.append( (f'L{myScope}','POR') )

    def checkMientras(self, node):
        myScope = self.scopes
        expr = node.children[0]
        sent = node.children[1]

        self.labels.append( (f'L{myScope}','MIENTRAS') )
        self.scopes+=1

        self.checkNode(expr)
        for child in sent.children:
            self.checkNode(child)
        
        self.labels.append( (f'L{myScope}','MIENTRAS') )

    def checkOpArit(self, node):
        left = node.children[0]
        op = node.children[1].value.get('value')
        right = node.children[2]

        #Check if the left value is an aritmetic operation
        if left.value == 'Operacion Aritmetica':
            left = self.checkOpArit(left)
        #Check if the left value is a dictionary,then it could be an identifier so we need to extract its value and assign it to left
        elif type(left.value) is dict:
            if left.value.get('category') == 'IDENTIFICADOR':
                #If left is a var, get the var value from the self.variables dictionary
                if left.value.get('value') in self.variables:
                    left = self.variables[left.value.get('value')]
                #If left is a var and it is not in the self.variables dictionary, throw an error
                else:
                    self.throwError(f'ERROR: Variable {left.value.get("value")} no declarada.')
            elif type(left) != Node:
                if type(left.get('value')) is tuple:
                    if left.get('value')[0] == 'Operacion Aritmetica':
                        left = self.checkOpArit(left.get('value')[1:])
                    elif left.get('value')[0] == 'Operacion Relacional':
                        left = self.checkOpRel(left.get('value')[1:])
                    elif left.get('value')[0] == 'Operacion Logica':
                        left = self.checkOpLog(left.get('value')[1:])
            else:
                #If left is a dictionary but not an identifier, just extract its value
                left = left.value

        #Check if the right value is an aritmetic operation
        if right.value == 'Operacion Aritmetica':
            right = self.checkOpArit(right)
        #Check if the right value is a dictionary,then it could be an identifier so we need to extract its value and assign it to left
        elif type(right.value) is dict:
            if right.value.get('category') == 'IDENTIFICADOR':
                #If right is a var, get the var value from the self.variables dictionary
                if right.value.get('value') in self.variables:
                    right = self.variables[right.value.get('value')]
                #If right is a var and it is not in the self.variables dictionary, throw an error
                else:
                    self.throwError(f'ERROR: Variable {right.value.get("value")} no declarada.')
            elif type(right) != Node:
                if type(right.get('value')) is tuple:
                    if right.get('value')[0] == 'Operacion Aritmetica':
                        right = self.checkOpArit(right.get('value')[1:])
                    elif right.get('value')[0] == 'Operacion Relacional':
                        right = self.checkOpRel(right.get('value')[1:])
                    elif right.get('value')[0] == 'Operacion Logica':
                        right = self.checkOpLog(right.get('value')[1:])
            else:
                #If right is a dictionary but not an identifier, just extract its value 
                right = right.value

        #Check value
        if left.get('value') == 'NULO' or right.get('value') == 'NULO':
            self.throwError(f'ERROR: Valores incompatibles para realizar operacion. {left.get("value")} y {right.get("value")}')
        elif left.get('category') == right.get('category'):
            if op == '+':
                result = { 'category': left.get('category'), 'value': left.get('value') + right.get('value') }
            if op == '-':
                result = { 'category': left.get('category'), 'value': left.get('value') - right.get('value') }
            if op == '*':
                result = { 'category': left.get('category'), 'value': left.get('value') * right.get('value') }
            if op == '/':
                if left.get('category') == 'ENTERO':
                    result = { 'category': left.get('category'), 'value': int(left.get('value') / right.get('value')) }
                elif left.get('category') == 'DECIMAL':
                    result = { 'category': left.get('category'), 'value': float(left.get('value') / right.get('value')) }
        elif (left.get('category') == 'ENTERO' or left.get('category') == 'DECIMAL') and (right.get('category') == 'ENTERO' or right.get('category') == 'DECIMAL'):
            if op == '+':
                result = { 'category': 'ENTERO' if type(left.get('value') + right.get('value')) is int else 'DECIMAL', 'value': left.get('value') + right.get('value') }
            if op == '-':
                result = { 'category': 'ENTERO' if type(left.get('value') - right.get('value')) is int else 'DECIMAL', 'value': left.get('value') - right.get('value') }
            if op == '*':
                result = { 'category': 'ENTERO' if type(left.get('value') * right.get('value')) is int else 'DECIMAL', 'value': left.get('value') * right.get('value') }
            if op == '/':
                result = { 'category': 'ENTERO' if type(left.get('value') * right.get('value')) is int else 'DECIMAL', 'value': left.get('value') / right.get('value') }
        else:
            self.throwError(f'ERROR: No se pudo ejecutar la operación con valores incompatibles {left.get("category")} y {right.get("category")}.')
    
        self.labels.append( (op,left.get('value'),right.get('value'),f'T{self.tempVars}') )
        self.tempVars+=1
        return result

    def checkOpRel(self, node):
        left = node.children[0]
        op = node.children[1].value.get('value')
        right = node.children[2]

        #Check if the left value is an aritmetic operation
        if left.value == 'Operacion Aritmetica':
            left = self.checkOpArit(left)
        elif left.value == 'Operacion Relacional':
            left = self.checkOpRel(left)
        elif left.value == 'Operacion Logica':
            left = self.checkOpLog(left)
        #Check if the left value is a dictionary,then it could be an identifier so we need to extract its value and assign it to left
        elif type(left.value) is dict:
            if left.value.get('category') == 'IDENTIFICADOR':
                #If left is a var, get thgete var value from the self.variables dictionary
                if left.value.get('value') in self.variables:
                    left = self.variables[left.value.get('value')]
                #If left is a var and it is not in the self.variables dictionary, throw an error
                else:
                    self.throwError(f'ERROR: Variable {left.value.get("value")} no declarada.')
            elif type(left) != Node:
                if type(left.get('value')) is tuple:
                    if left.get('value')[0] == 'Operacion Aritmetica':
                        left = self.checkOpArit(left.get('value')[1:])
                    elif left.get('value')[0] == 'Operacion Relacional':
                        left = self.checkOpRel(left.get('value')[1:])
                    elif left.get('value')[0] == 'Operacion Logica':
                        left = self.checkOpLog(left.get('value')[1:])
            else:
                #If left is a dictionary but not an identifier, just extract its value
                left = left.value

        #Check if the right value is an aritmetic operation
        if right.value == 'Operacion Aritmetica':
            right = self.checkOpArit(right)
        elif right.value == 'Operacion Relacional':
            right = self.checkOpRel(right)
        elif right.value == 'Operacion Logica':
            right = self.checkOpLog(right)
        #Check if the right value is a dictionary,then it could be an identifier so we need to extract its value and assign it to right
        elif type(right.value) is dict:
            if right.value.get('category') == 'IDENTIFICADOR':
                #If right is a var, get the var value from the self.variables dictionary
                if right.value.get('value') in self.variables:
                    right = self.variables[right.value.get('value')]
                #If right is a var and it is not in the self.variables dictionary, throw an error
                else:
                    self.throwError(f'ERROR: Variable {right.value.get("value")} no declarada.')
            else:
                #If right is a dictionary but not an identifier, just extract its value
                right = right.value

        #Check value
        if left.get('category') == right.get('category'):
            if op == '=':
                result = { 'category': 'TIPO_BOOLEANO', 'value': 'VERDADERO' if left.get('value') == right.get('value') else 'FALSO' }
            elif op == '<':
                result = { 'category': 'TIPO_BOOLEANO', 'value': 'VERDADERO' if left.get('value') < right.get('value') else 'FALSO' }
            elif op == '>':
                result = { 'category': 'TIPO_BOOLEANO', 'value': 'VERDADERO' if left.get('value') > right.get('value') else 'FALSO' }
            elif op == '<=':
                result = { 'category': 'TIPO_BOOLEANO', 'value': 'VERDADERO' if left.get('value') <= right.get('value') else 'FALSO' }
            elif op == '>=':
                result = { 'category': 'TIPO_BOOLEANO', 'value': 'VERDADERO' if left.get('value') >= right.get('value') else 'FALSO' }
            elif op == '?':
                result = { 'category': 'TIPO_BOOLEANO', 'value': 'VERDADERO' if left.get('value') != right.get('value') else 'FALSO' }
        else:
            self.throwError(f'ERROR: No se pudo ejecutar la operación con valores incompatibles {left.get("category")} y {right.get("category")}.')

        self.labels.append( (op,left.get('value'),right.get('value'),f'T{self.tempVars}') )
        self.tempVars+=1
        return result

    def checkOpLog(self, node):
        left = node.children[0]
        op = node.children[1].value.get('value')
        right = node.children[2]

        #Check left
        if left.value == 'Operacion Aritmetica':
            left = self.checkOpArit(left)
        elif left.value == 'Operacion Relacional':
            left = self.checkOpRel(left)
        elif left.value == 'Operacion Logica':
            left = self.checkOpLog(left)
        #Check if the left value is a dictionary,then it could be an identifier so we need to extract its value and assign it to left
        elif type(left.value) is dict:
            if left.value.get('category') == 'IDENTIFICADOR':
                #If left is a var, get the var value from the self.variables dictionary
                if left.value.get('value') in self.variables:
                    left = self.variables[left.value.get('value')]
                #If left is a var and it is not in the self.variables dictionary, throw an error
                else:
                    self.throwError(f'ERROR: Variable {left.value.get("value")} no declarada.')
            else:
                #If left is a dictionary but not an identifier, just extract its value
                left = left.value

        #Check right
        if right.value == 'Operacion Aritmetica':
            right = self.checkOpArit(right)
        elif right.value == 'Operacion Relacional':
            right = self.checkOpRel(right)
        elif right.value == 'Operacion Logica':
            right = self.checkOpLog(right)
        #Check if the right value is a dictionary,then it could be an identifier so we need to extract its value and assign it to right
        elif type(right.value) is dict:
            if right.value.get('category') == 'IDENTIFICADOR':
                #If right is a var, get the var value from the self.variables dictionary
                if right.value.get('value') in self.variables:
                    right = self.variables[right.value.get('value')]
                #If right is a var and it is not in the self.variables dictionary, throw an error
                else:
                    self.throwError(f'ERROR: Variable {right.value.get("value")} no declarada.')
            else:
                #If right is a dictionary but not an identifier, just extract its value
                right = right.value

        #Check value
        try:
            if op == '&':
                result = { 'category': 'BOOLEANO', 'value': 'VERDADERO' if left.get('value') and right.get('value') else 'FALSO' }
            elif op == '|':
                result = { 'category': 'BOOLEANO', 'value': 'VERDADERO' if left.get('value') or right.get('value') else 'FALSO' }
        except:
            self.throwError(f'No se logró realzar la operación "{op}" entre {left} y {right}.')
        
        self.labels.append( (op,left.get('value'),right.get('value'),f'T{self.tempVars}') )
        self.tempVars+=1
        return result