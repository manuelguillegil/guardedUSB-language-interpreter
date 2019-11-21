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
        for i in range(len(varList)):
            if self.table.get(varList[i][0]) is None:
                self.table[varList[i][0]] = varList[i][1]
            else:
                print("La variable " + varList[i][0] + " ha sido declarada dos veces en el mismo bloque")
                sys.exit()

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

    # def checkArrayConsult(self, stack):
    #     if self.children[0].category == "Ident":
    #         var = self.children[0].searchTables(stack)
    #         if var is not None:
    #             arrInfo = var.split("[")
    #             if arrInfo[0] == "array":

    # def checkFunction(self, stack):
    #     if self.children[0].category == "Ident":
    #         var = self.children[0].searchTables(stack)
    #         if var is not None:
    #             arrInfo = var.split("[")
    #             if arrInfo[0] == "array":
    #                 if self.value == "atoi":
    #                     arrSize = arrInfo[1].split("..")
    #                     arrSize[1] = arrSize[1].split("]")[0]
    #                     if (int(arrSize[1]) - int(arrSize[0]) + 1) == 1:
    #                         return True
    #                     else:
    #                         print("El arreglo " + self.children[0].getValue() + " tiene más de un elemento\
    #                             la función atoi() no se puede invocar")
    #                         sys.exit()
    #                 else:
    #                     return True
    #             else:
    #                 print("La variable " + self.children[0].getValue() + " no representa un arreglo. La función\
    #                     utilizada no es aplicable")
    #                 sys.exit()
    #         else:
    #             print("Error: Variable " + self.children[0].value + " no declarada")
    #             sys.exit()
    #     else:


    
    # def checkArithmeticExp(self, stack):
    #     if self.category == "AritOp":
    #         return self.children[0].checkArithmeticExp(stack) and self.children[1].checkArithmeticExp(stack)
    #     elif self.category == "UnaryMinus":
    #         return self.children[0].checkArithmeticExp(stack)
    #     elif self.category == "Function":
    #         return self.checkFunction(stack)
    #     elif self.category == "ArrayOp" and self.value == "ArrayConsult":
    #         return self.checkArrayConsult(stack)

    # def checkStaticErrors(self):
    #     tableStack = []
    #     return self.checkStaticErrorsAux(tableStack)

    # def checkStaticErrorsAux(self, stack):
    #     if isinstance(self, BlockNode):
    #         if not bool(self.symbol_table.getTable()): #Si el bloque tiene variables declaradas
    #             stack.insert(0, self.symbol_table)  #Insertamos la nueva tabla de símbolos
    #             if (len(self.children) == 2): #Si hay solo una instrucción
    #                 return self.children[1].checkStaticErrorsAux(stack)
    #             else:
    #                 stackLength = len(stack) #Si hay una secuencia de instrucciones debemos guardar el tamaño del
    #                                          #stack ya que este puede variar dentro de la siguiente instrucción
    #                 child1 = self.children[1].checkStaticErrorsAux(stack)
    #                 while len(stack) != stackLength: #Si el stack vario lo devolvemos alestado en que estaba originalmente
    #                     stack.pop(0)
    #                 child2 = self.children[2].checkStaticErrorsAux(stack)

    #                 return child1 and child2
    #         else:
    #             return self.children[0].checkStaticErrorsAux()
    #     elif self.category == "Asig":
    #         tipo = self.children[0].searchTables(stack)
    #         if tipo is not None:
    #             if tipo == "int":
    #                 return self.children[1].checkArithmeticExp(stack)
    #             elif tipo == "bool":
    #                 return self.children[1].checkBoolExp(stack)
    #             else:
    #                 return self.children[1].checkArrayExp(stack)
    #         else:
    #             print("Error: Variable " + self.children[0].value + " no declarada")

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

class BlockNode(Node):
    
    def __init__(self, category, value, children=None, varList=None):
        super().__init__(category, value, children)
        self.symbol_table = Symbol_Table()
        self.symbol_table.fillTable(varList)
