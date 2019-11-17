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

## Creamos un objeto que será nuestro arbol que guardará todo los nodos generados en una lista 
### y tendrá una o las tablas de simbolos correspondientes
class ASTree:
    def __init__(self):
        self.node_list = []
        self.simbol_table = Hash_table()

    def setNode(self, Node):
        self.node_list.append(Node)

    def setNodeWithSimbol(self, Node, Simbol):
        self.node_list.append(Node)
        self.simbol_table.insert(Simbol)
    
    ## Esta logica todavía le falta mucho jeje
    def updateSimbol(self, Simbol):
        index = self.simbol_table.search(Simbol)
        if index is not None:
            self.remove(Simbol)
            self.insert(Simbol)


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
        else:
            print(indent + self.value)

        for i in range(len(self.children)):
            self.children[i].printTree(indent + " ")

    def findValue(self):
        if (self.category == "Literal" or self.category == "Ident"):
            return self.value
        else: 
            for i in range(len(self.children)):
                self.children[i].findValue()

    def findDataType(self):
        pass

class DecNode(Node):
    def __init__(self, category, value, children=None, last=None):
        super().__init__(category, value, children)
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

class Simbol:
    def __init__(self, variable, data_type, value):
        self.variable = variable
        self.value = value
        self.data_type = data_type

    def setVariable(variable):
        self.variable = variable
    
    def setDataType(data_type):
        self.data_type = data_type

    def setValue(value):
        self.value = value

class Hash_table:
    def __init__(self):
        self.table = [None] * 127
    
    # Función hash
    def hash_func(self, value):
        key = 0
        for i in range(0,len(value.variable)):
            key += ord(value.variable[i])
        return key % 127

    def insert(self, value): # Metodo para ingresar elementos
        hash = self.hash_func(value)
        if self.table[hash] is None:
            self.table[hash] = value
   
    def search(self,value): # Metodo para buscar elementos
        hash = self.hash_func(self, value)
        if self.table[hash] is None:
            return None
        else:
            return hex(id(self.table[hash]))
  
    def remove(self,value): # Metodo para eleminar elementos
        hash = self.hash_func(value)
        if self.table[hash] is None:
            print("No hay elementos con ese valor", value)
        else:
            print("Elemento con valor", value, "eliminado")
            self.table[hash] is None