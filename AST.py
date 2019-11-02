##Proyecto Traductores e Interpretadores, CI-3725
##Entrega 2
##Manuel Gil, 14-10397
##Diego Peña, 15-11095
##Fecha de inicio: 28-09-2019, 21:16 Hora de Venezuela
##Fecha de modificación: 01-11-2019, 08:16 Hora de Venezuela

##Actualización: Estructura básica de los nodos del AST. ES probable que falten cosas o que no esté del todo bien
#En principio category nos indica la regla que se está aplicando y en value va una tupla (Tipo,valor) donde tio indica el
##tipo de la variable y valor en valor como tal. En algunos casos simplemente hay valor. No estoy muy claro como funcionará
##en operadores

class Node:

    def __init__(self, category, value, children=None):
        self.category = category
        self.value = value
        if children:
            self.children = children
        else:
            self.children = []

    def printTree(self):

        if (self.category == "Ident"):
            print(self.category + " " + self.value)
        else:
            print(self.value)

        for i in range(len(self.children)):
            printTree(self.children[i])



        