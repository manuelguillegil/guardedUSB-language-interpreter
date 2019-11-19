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

class Symbol:
    def __init__(self, var, data_type, value):
        self.var = var
        self.value = value
        self.data_type = data_type

    def setVariable(self, variable):
        self.variable = variable
    
    def setDataType(self, data_type):
        self.data_type = data_type

    def setValue(self, value):
        self.value = value

    def printSymbol(self):
        print("Simbolo: VAR: " + str(self.var) + " data_type: " + str(self.data_type) + " value: " + str(self.value))

class Symbol_Table:
    def __init__(self):
        self.symbol_table = Hash_Table()

    def setSymbol(self, Symbol):
        self.symbol_table.insert(Symbol)
        Symbol.printSymbol()

    def setValue(self, variable, ChildrenNodeExpresion):
        index = self.symbol_table.searchByVariable(variable)
        value = ChildrenNodeExpresion.findValue()
        if value is not None:
            print('index en la tabla de hash: ' + index + ' y valor que se le asigna: ' + value)
            ## Hay que ver aquí como buscar el DataType de la variable asociada
            symbol = self.symbol_table.searchByVariableTheSymbol(variable)
            self.symbol_table.remove(symbol)
            self.symbol_table.insert(Symbol(variable, symbol.data_type, value))
            Symbol(variable, symbol.data_type, value).printSymbol()

class Node:
    def __init__(self, category, value, children=None):
        self.category = category
        self.value = value
        self.expresionValue = ''
        if children:
            self.children = children
        else:
            self.children = []

    def printTree(self, indent):

        if (self.category == "Ident" or self.category == "Literal"):
            print(indent + self.category + " " + str(self.value))
        else:
            print(indent + self.value)

        for i in range(len(self.children)):
            self.children[i].printTree(indent + " ")

    def findValue(self):
        if (self.category == "Literal" or self.category == "Ident"):
            return str(self.value)
        else: 
            for i in range(len(self.children)):
                self.children[i].findValue()
                return self.children[i].findValue()

    def findDataType(self):
        pass

class DecNode(Node):
    def __init__(self, category, value, tupleList, children=None, last=None):
        super().__init__(category, value, children)
        self.declaredVars = tupleList
        self.lastLine = last

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

class Hash_Table:
    def __init__(self):
        self.table = [None] * 127
    
    # Función hash
    def hash_func(self, value):
        key = 0
        for i in range(0,len(value.var)):
            key += ord(value.var[i])
        return key % 127

    def insert(self, Symbol): # Metodo para ingresar elementos
        hash = self.hash_func(Symbol)
        if self.table[hash] is None:
            self.table[hash] = Symbol

    ## Ambos métodos de search solo nos devuelve el index en donde está el elemento. Esto nos sirve al menos para saber que si está
    ### en la tabla de hash (esto pareciera más un exists que un search)
    def search(self,value): # Metodo para buscar elementos considerando los tres campos de un símbolo
        hash = self.hash_func(value)
        if self.table[hash] is None:
            return None
        else:
            return hex(id(self.table[hash]))
    
    def searchByVariable(self,variable): # Metodo para buscar elementos
        ## No importa saber el tipo de dato y valor en el simbolo al momento de buscar por la variable
        ### ya que hash_func solo toma en cuenta la variable en un simbolo
        simbolo = Symbol(variable, None, None)
        hash = self.hash_func(simbolo)
        if self.table[hash] is None:
            return None
        else:
            return hex(id(self.table[hash]))

    def searchByVariableTheSimbol(self,variable): # Metodo para buscar elementos
        ## No importa saber el tipo de dato y valor en el simbolo al momento de buscar por la variable
        ### ya que hash_func solo toma en cuenta la variable en un simbolo
        simbolo = Symbol(variable, None, None)
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