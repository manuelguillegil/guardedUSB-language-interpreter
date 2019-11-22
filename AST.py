##Proyecto Traductores e Interpretadores, CI-3725
##Entrega 3
##Manuel Gil, 14-10397
##Diego Peña, 15-11095
##Fecha de inicio: 28-09-2019, 21:16 Hora de Venezuela
##Fecha de modificación: 03-11-2019 en lamañana

##Actualización: Estructura básica de los nodos del AST. ES probable que falten cosas o que no esté del todo bien
#En principio category nos indica la regla que se está aplicando y en value va una tupla (Tipo,valor) donde tio indica el
##tipo de la variable y valor en valor como tal. En algunos casos simplemente hay valor. No estoy muy claro como funcionará
##en operadore

import sys

class Symbol_Table:
    def __init__(self):
        self.table ={}

    def fillTable(self, varList):
        if varList is not None:
            for i in range(len(varList)):
                if self.table.get(varList[i][0]) is None:
                    self.table[varList[i][0]] = varList[i][1]
                else:
                    print("La variable " + varList[i][0] + " ha sido declarada dos veces en el mismo bloque")
                    sys.exit()

    ## Falta comprobar que esta variable no se encuentre en otros ForNode's que envuelvan a este For
    def fillTableFor(self, var):
        if var is not None:
            self.table[var] = var

    def printSymbolTable(self, indent):
        print(indent + "Symbol table")
        infoIndent = indent + " "
        iterator = iter(self.table)
        for key in iterator:
            print(infoIndent + "variable: " + key + " | type: " +  self.table[key])

    def getValue(self, key):
        return self.table[key]

    def getTable(self):
        return self.table

class Node:
    def __init__(self, category, value, children=None):
        self.category = category
        self.value = value
        if children:
            self.children = children
        else:
            self.children = []

    def printTree(self, indent):

        if (self.category == "Ident" or self.category == "Literal"):
            print(indent + self.category + " " + str(self.value))
        elif isinstance(self, BlockNode):
            print(indent + self.value)
            self.symbol_table.printSymbolTable(indent + " ")
        else:
            print(indent + self.value)

        for i in range(len(self.children)):
            self.children[i].printTree(indent + " ")

    def searchTables(self, symbolTableStack):
        for i in range(len(symbolTableStack)):
            value = symbolTableStack[i].getValue(self.value)
            if value is not None:
                return value
        return value

    def searchForTables(self, symbolForTableStack):
        for i in range(len(symbolForTableStack)):
            value = symbolForTableStack[i].getValue(self.value)
            if value is not None:
                return False
        return True

    def checkArrayConsult(self, stack):
        if self.children[0].category == "Ident":
            var = self.children[0].searchTables(stack)
            if var is not None:
                arrInfo = var.split("[")
                if arrInfo[0] == "array":
                    return self.children[1].checkArithmeticExp(stack)
                else:
                    print("Error: La variable " + self.children[0].value + " es de tipo " + arrInfo[0]\
                        + ". Las consultas solo están permitidas sobre los elementos de tipo array")
            else:
                print("Error: Variable " + self.children[0].value + " no declarada")
        elif self.children[0].category == "ArrayOp" and self.children[0].value == "ArrayAsig":
            self.children[0].checkFunction(stack)
        else:
            print("Error: No estoy muy claro que representaría este error")

    #Verificación de que el parámetro que se le pasa a la función sea un arreglo
    def checkFunction(self, stack, function):
        if self.children[0].category == "Ident":
            var = self.children[0].searchTables(stack)
            if var is not None:
                arrInfo = var.split("[")
                if arrInfo[0] == "array":
                    if function == "atoi":
                        arrSize = arrInfo[1].split("..")
                        arrSize[1] = arrSize[1].split("]")[0]
                        if (int(arrSize[1]) - int(arrSize[0]) + 1) == 1:
                            self.children[0]
                        else:
                            print("El arreglo " + self.children[0].getValue() + " tiene más de un elemento\
                                la función atoi() no se puede invocar")
                            sys.exit()
                    else:
                        return True
                else:
                    print("La variable " + self.children[0].getValue() + " no representa un arreglo. La función\
                        utilizada no es aplicable")
                    sys.exit()
            else:
                print("Error: Variable " + self.children[0].value + " no declarada")
                sys.exit()
        elif self.children[0].category == "ArrayOp" and self.children[0].value == "ArrayAsig":
            self.children[0].checkFunction(stack, function)
        else:
            print("Error: El parámetro de la función no es del tipo soportado por la misma (array)")

    #NO ESTÁ COMPLETA FALTA CASO BASE
    def checkArithmeticExp(self, stack):
        if self.category == "AritOp":
            return self.children[0].checkArithmeticExp(stack) and self.children[1].checkArithmeticExp(stack)
        elif self.category == "UnaryMinus":
            return self.children[0].checkArithmeticExp(stack)
        elif self.category == "Function":
            return self.checkFunction(stack, self.value)
        elif self.category == "ArrayOp" and self.value == "ArrayConsult":
            return self.checkArrayConsult(stack)

    def checkStaticErrors(self):
        tableStack = []
        forTableStack = []
        return self.checkStaticErrorsAux(tableStack, forTableStack)

    def checkStaticErrorsAux(self, stack, forTableStack):
        if isinstance(self, BlockNode):
            if not bool(self.symbol_table.getTable()): #Si el bloque tiene variables declaradas
                stack.insert(0, self.symbol_table)  #Insertamos la nueva tabla de símbolos
                if (len(self.children) == 2): #Si hay solo una instrucción
                    return self.children[1].checkStaticErrorsAux(stack, forTableStack)
                else:
                    stackLength = len(stack) #Si hay una secuencia de instrucciones debemos guardar el tamaño del
                                             #stack ya que este puede variar dentro de la siguiente instrucción
                    child1 = self.children[1].checkStaticErrorsAux(stack, forTableStack)
                    while len(stack) != stackLength: #Si el stack varió lo devolvemos al estado en que estaba originalmente
                        stack.pop(0)
                    child2 = self.children[2].checkStaticErrorsAux(stack, forTableStack)

                    return child1 and child2
            else:
                return self.children[0].checkStaticErrorsAux()
        elif isinstance(self, ForNode):
            forTableStack.insert(0, self.symbol_table)  #Insertamos la nueva tabla de símbolos
        elif self.category == "Asig":
            if self.children[0].searchForTables(forTableStack): #Verificamos si la variable está dentro de la tabla de For
                tipo = self.children[0].searchTables(stack)
                if tipo is not None:
                    if tipo == "int":
                        return self.children[1].checkArithmeticExp(stack)
                    elif tipo == "bool":
                        return self.children[1].checkBoolExp(stack)
                    else:
                        return self.children[1].checkArrayExp(stack)
                else:
                    print("Error: Variable " + self.children[0].value + " no declarada")
            else:
                print("Se está cambiando el valor de una variable iterable del for: " + self.children[0].value)
        ## Chequeamos que el body y la lista de guardias del if la expresión sea booleana
        elif self.category == "Body" or self.category == "GuardList":
                if self.children[1].checkBoolExp(stack): ## Si la expresión corresponde con un bool, entonces seguimos
                    if (len(self.children) > 2):  ### y seguimos chequeando los StaticErrors de las instrucciones y guardias
                        child1 = self.children[2].checkStaticErrorsAux(stack, forTableStack) ## Chequeamos errores staticos de las instrucciones
                        child2 = self.children[3].checkStaticErrorsAux(stack, forTableStack) ## Ahora para las demás guardias
                        return child1 and child2
                    else: 
                        return self.children[2].checkStaticErrorsAux(stack, forTableStack) ## No hay más guardias, así que solo chequeamos las instrucciones
                else:
                    print("Error: La expresión " + self.children[1].value + " no es de tipo bool para una guardia del If")


    def getValue(self):
        return self.value

class DecNode(Node):
    def __init__(self, category, value, tupleList, children=None, last=None):
        super().__init__(category, value, children)
        self.declaredVars = tupleList
        self.lastLine = last

    def getDeclaredVars(self):
        return self.declaredVars

    #Esto me permite que cada línea de declaración se vea como hija de la línea anterior
    def addChildren(self, newChildren):
        if self.lastLine: #Si esta es la última línea de declaración leída, el hijo va aquí
            sequence = len(self.children) #Esta es la ubicación en la lista de hijos donde va el nuevo hijo
            self.lastLine = False #Esta ya no es la última línea declarada
            self.children = self.children + newChildren
            self.children[sequence].children[0].lastLine = True
        else: #Si no, debemos revisar la siguiente línea
            sequence = len(self.children) - 1 #Ubicación en la lista de hijos donde va el nodo secuenciación
            self.children[sequence].children[0].addChildren(newChildren)

    #Une la lista de tuplas de una línea de declaración con la de la línea siguiente, de manera que el block pueda
    #usar esta lista para crear la tabla de símbolos correspondiente a todas las declaraciones
    def addTupleList(self, newTuples):
        self.declaredVars += newTuples

class ForNode(Node):
    
    def __init__(self, category, value, children=None, var=None):
        super().__init__(category, value, children)
        self.symbol_table = Symbol_Table()
        self.symbol_table.fillTableFor(var)

class BlockNode(Node):
    
    def __init__(self, category, value, children=None, varList=None):
        super().__init__(category, value, children)
        self.symbol_table = Symbol_Table()
        self.symbol_table.fillTable(varList)
