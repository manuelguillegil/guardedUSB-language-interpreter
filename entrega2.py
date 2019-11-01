##Proyecto Traductores e Interpretadores, CI-3725
##Entrega 2
##Manuel Gil, 14-10397
##Diego Peña, 15-11095
##Fecha de inicio: 28-09-2019, 19:44 Hora de Venezuela
##Fecha de modificación: 01-11-2019, 08:16 Hora de Venezuela

#Actualización: CReo que ya más o menos sé que hacer con el árbol

#Pendiente: Resolver lo de MultipleTypeDeclaration

from lexer import CustomLexer
from AST import Node
import ply.yacc as yacc
import re
import sys

def p_ProgramBlock(p):
    '''ProgramBlock : TkOBlock Declaration TkCBlock'''
    p[0] = Node("Block", "Block", [p[1]])
    

def p_Declaracion(p):
    '''Declaration : TkDeclare DeclareLines'''

def p_DeclareLinesMultiple(p):
    '''DeclareLines: VarDeclaration TkSemiColon DeclareLines
                   | VarDeclaration'''

def p_VarDeclaration(p):
    '''VarDeclaration: MultipleTypeDeclaration
                     | SingleTypeDeclaration'''

def p_SingleTypeDeclaration(p):
    '''SingleTypeDeclaration : IdList TkTwoPoints IdType'''

def p_IdType(p):
    '''IdType : TkInt
              | TkBool
              | TkArray TkOBrackets TkNumber TkSoForth TkNumber TkCBrackets'''

def p_IdList(p):
    '''IdList : TkId TkComma IdList
              | TkId'''


############## MAIN ####################

#Nos aseguramos de que haya un arcghivo de input
try:
    assert(len(sys.argv) > 1)
except:
    print("No hay archivo de input")
    sys.exit()

#Nos aseguramos de que el archivo input tenga la extensión requerida
try:
    #Si la extensión es correcta, entonces extension = .gusb
    extension = sys.argv[1][len(sys.argv[1]) - 5: len(sys.argv[1])]
    assert('.gusb' in extension)
except:
    print("Este tipo de archivo no es reconocido")
    sys.exit()

#### MAIN ####

# Construir el lexer
lexer = CustomLexer()
lexer.build()
tokens = lexer.tokens
parser = yacc.yacc()

with open(sys.argv[1]) as fp:
    parser.parse(fp.read(), lexer = lexer.lexer)
fp.closed