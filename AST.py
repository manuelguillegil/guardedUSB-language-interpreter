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

<<<<<<< HEAD
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
=======
class Simbol:
    def __init__(self, var, data_type):
        self.var = var
        # self.value = value
        self.data_type = data_type

    def setVariable(self, variable):
        self.variable = variable
    
    def setDataType(self, data_type):
        self.data_type = data_type

    # def setValue(value):
    #    self.value = value

    def printSimbol(self):
        print("Simbolo: VAR: " + str(self.var) + " data_type: " + str(self.data_type)

class Symbol_Table:
    def __init__(self):
        self.symbol_table = Hash_Table()

    def setSymbol(self, Symbol):
        self.symbol_table.insert(Symbol)
        Symbol.printSymbol()

    # def setValue(self, variable, ChildrenNodeExpresion):
    #     index = self.simbol_table.searchByVariable(variable)
    #     value = ChildrenNodeExpresion.findValue()
    #     if value is not None:
    #         print('index en la tabla de hash: ' + index + ' y valor que se le asigna: ' + value)
    #         ## Hay que ver aquí como buscar el DataType de la variable asociada
    #         simbol = self.simbol_table.searchByVariableTheSimbol(variable)
    #         self.simbol_table.remove(simbol)
    #         self.simbol_table.insert(Simbol(variable, simbol.data_type, value))
    #         Simbol(variable, simbol.data_type, value).printSimbol()
>>>>>>> a17e2f7de15560538465e3381a2754cec3f85e93

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
    
<<<<<<< HEAD
    def __init__(self, category, value, children=None, varList=None):
        super().__init__(category, value, children)
        self.symbol_table = Symbol_Table()
        self.symbol_table.fillTable(varList)
=======
    def searchByVariable(self,variable): # Metodo para buscar elementos
        ## No importa saber el tipo de dato y valor en el simbolo al momento de buscar por la variable
        ### ya que hash_func solo toma en cuenta la variable en un simbolo
        simbolo = Simbol(variable, None)
        hash = self.hash_func(simbolo)
        if self.table[hash] is None:
            return None
        else:
            return hex(id(self.table[hash]))

    def searchByVariableTheSimbol(self,variable): # Metodo para buscar elementos
        ## No importa saber el tipo de dato y valor en el simbolo al momento de buscar por la variable
        ### ya que hash_func solo toma en cuenta la variable en un simbolo
        simbolo = Simbol(variable, None)
        hash = self.hash_func(simbolo)
        if self.table[hash] is None:
            return None
        else:
            return self.table[hash]
  
    def remove(self,value): # Metodo para eleminar elementos. Solo basta buscar el index de la tabla de hash considerando la variable del símbolo
        hash = self.hash_func(value)
        if self.table[hash] is None:
            print("No hay elementos con ese valor", str(value.var))
        else:
            self.table[hash] = None
>>>>>>> a17e2f7de15560538465e3381a2754cec3f85e93
