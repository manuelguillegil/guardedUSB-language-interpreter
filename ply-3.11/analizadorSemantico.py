##Proyecto Traductores e Interpretadores, CI-3725
##Entrega 3 - Analizador Semántico
##Manuel Gil, 14-10397
##Diego Peña, 15-11095
##Fecha de inicio: 13-11-2019
##Fecha de modificación: 13-11-2019 

#Actualización: 

from CustomLexer import CustomLexer
from AST import Node, DecNode
import ply.yacc as yacc
import re
import sys

txt = " "
cont = 0
def incrementarContador():
    global cont
    cont += 1
    return "%d" %cont 

class Start(Node):
    def __init__(self, name):
        self.name = name
    
    def traducir(self):
        global txt
        id = incrementarContador()

        return id

class ProgramBlock(Node):
    def __init__(self, name):
        self.name = name
    
    def traducir(self):
        global txt
        id = incrementarContador()

        return id

class DeclareLines(Node):
    def __init__(self, name):
        self.name = name
    
    def traducir(self):
        global txt
        id = incrementarContador()

        return id

class VarDeclaration(Node):
    def __init__(self, name):
        self.name = name
    
    def traducir(self):
        global txt
        id = incrementarContador()

        return id

class MultipleTypeDeclaration(Node):
    def __init__(self, name):
        self.name = name
    
    def traducir(self):
        global txt
        id = incrementarContador()

        return id

class SingleTypeDeclaration(Node):
    def __init__(self, name):
        self.name = name
    
    def traducir(self):
        global txt
        id = incrementarContador()

        return id

class IdType(Node):
    def __init__(self, name):
        self.name = name
    
    def traducir(self):
        global txt
        id = incrementarContador()

        return id

class Instructions(Node):
    def __init__(self, name):
        self.name = name
    
    def traducir(self):
        global txt
        id = incrementarContador()

        return id

class InstSequence(Node):
    def __init__(self, name):
        self.name = name

    def traducir(self):
        global txt
        id = incrementarContador()

        return id 

class InstructionLine(Node):
    def __init__(self, name):
        self.name = name
    
    def traducir(self):
        global txt
        id = incrementarContador()

        return id

class Asig(Node):
    def __init__(self, name):
        self.name = name
    
    def traducir(self):
        global txt
        id = incrementarContador()

        return id

class IfDo(Node):
    def __init__(self, name):
        self.name = name
    
    def traducir(self):
        global txt
        id = incrementarContador()

        return id

class Printing(Node):
    def __init__(self, name):
        self.name = name
    
    def traducir(self):
        global txt
        id = incrementarContador()

        return id

class Read(Node):
    def __init__(self, name):
        self.name = name
    
    def traducir(self):
        global txt
        id = incrementarContador()

        return id

class Concat(Node):
    def __init__(self, name):
        self.name = name
    
    def traducir(self):
        global txt
        id = incrementarContador()

        return id

class Body(Node):
    def __init__(self, name):
        self.name = name
    
    def traducir(self):
        global txt
        id = incrementarContador()

        return id

class GuardList(Node):
    def __init__(self, name):
        self.name = name
    
    def traducir(self):
        global txt
        id = incrementarContador()

        return id

class For(Node):
    def __init__(self, name):
        self.name = name
    
    def traducir(self):
        global txt
        id = incrementarContador()

        return id

class In(Node):
    def __init__(self, name):
        self.name = name
    
    def traducir(self):
        global txt
        id = incrementarContador()

        return id

class ExpAux(Node):
    def __init__(self, name):
        self.name = name
    
    def traducir(self):
        global txt
        id = incrementarContador()

        return id

class Value(Node):
    def __init__(self, name):
        self.name = name
    
    def traducir(self):
        global txt
        id = incrementarContador()

        return id

class Function(Node):
    def __init__(self, name):
        self.name = name
    
    def traducir(self):
        global txt
        id = incrementarContador()

        return id

class AbsValue(Node):
    def __init__(self, name):
        self.name = name
    
    def traducir(self):
        global txt
        id = incrementarContador()

        return id

class error(Node):
    def __init__(self, name):
        self.name = name
    
    def traducir(self):
        global txt
        id = incrementarContador()

        return id