##Proyecto Traductores e Interpretadores, CI-3725
##Entrega 2
##Manuel Gil, 14-10397
##Diego Peña, 15-11095
##Fecha de inicio: 28-09-2019, 19:44 Hora de Venezuela
##Fecha de modificación: 01-11-2019, 21:04 Hora de Venezuela

#Actualización: Resolví lo de MultipleTypeDeclaration, pero no lo del árbol

from lexer import CustomLexer
from AST import Node
import ply.yacc as yacc
import re
import sys

def p_ProgramBlock(p):
    '''ProgramBlock : TkOBlock Declaration TkCBlock'''
    p[0] = Node("ProgramBlock", "Block", [p[2]])
    

def p_Declaration(p):
    '''Declaration : TkDeclare DeclareLines'''
    p[0] = p[1]

def p_DeclareLines(p):
    '''DeclareLines : VarDeclaration DeclarationSequence
                    | VarDeclaration'''
    if(len(p) == 4):
        p[0] = Node("DeclareLines", "Declare", [p[1], p[2]])
    else:
        p[0] = Node("DeclareLines", "Declare", [p[1]])

def p_DeclarationSequence(p):
    '''DeclarationSequence : TkSemicolon VarDeclaration DeclarationSequence
                           | TkSemicolon VarDeclaration'''

    if (len(p) == 4):
        p[0] = Node("DeclarationSequence", "Sequence", [p[1], p[2]])
    else:
        p[0] = Node("DeclarationSequence", "Sequence", [p[1]])

def p_VarDeclaration(p):
    '''VarDeclaration : MultipleTypeDeclaration
                      | SingleTypeDeclaration'''

    p[0] = p[1]

def p_MultipleTypeDeclaration(p):
    '''MultipleTypeDeclaration : TkId TkComma MultipleTypeDeclaration TkComma IdType
                               | TkId TkTwoPoints TkComma'''
    if (len(p) == 6):
        p[3] = Node("Ident", p[1], [p[3]])
    else:
        p[3] = Node("Ident", p[1])

def p_SingleTypeDeclaration(p):
    '''SingleTypeDeclaration : TkId TkComma IdList TkTwoPoints IdType'''

    p[0] = Node("Ident", p[1], [p[3]])

def p_IdList(p):
    '''IdList : TkId TkComma IdList
              | TkId'''
    if(len(p) == 4):
        p[0] = Node("Ident", p[1], [p[3]])
    else:
        p[0] = Node("Ident", p[1])

def p_IdType(p):
    '''IdType : TkInt
              | TkBool
              | TkArray TkOBracket TkNum TkSoForth TkNum TkCBracket'''

def p_error(p):
    print("Syntax error in input!")


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