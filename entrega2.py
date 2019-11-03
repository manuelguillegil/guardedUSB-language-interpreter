##Proyecto Traductores e Interpretadores, CI-3725
##Entrega 2
##Manuel Gil, 14-10397
##Diego Peña, 15-11095
##Fecha de inicio: 28-09-2019, 00:07 Hora de Venezuela
##Fecha de modificación: 02-11-2019, 23:35 Hora de Venezuela

#Actualización: Resolví lo de MultipleTypeDeclaration, pero no lo del árbol
# Estoy tratando de hacer If, la guardia, bloque y For esencialmente
# Si If está listo, Do debería tener una logica similar
# Aunque For e In me están dando una recursión infinita (relacionada por In)
# y al quitarlos, me aparece un error en el Input por el If imprimiendome:
# Syntax error in input
# LexToken(TkIf,'if',5,37). Para el archivo .gusb de prueba2 
## También se añadieron algunas precedencias, en este caso para la artimética

from CustomLexer import CustomLexer
from AST import Node
import ply.yacc as yacc
import re
import sys

def p_ProgramBlock(p):
    '''ProgramBlock : TkOBlock Declaration Instructions TkCBlock'''
    p[0] = Node("ProgramBlock", "Block", [p[2], p[3]])
    print("Hey there")
    p[0].printTree()

def p_Declaration(p):
    '''Declaration : TkDeclare DeclareLines'''
    p[0] = p[2]

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
#| SingleTypeDeclaration

    p[0] = p[1]

def p_MultipleTypeDeclaration(p):
    '''MultipleTypeDeclaration : TkId TkComma MultipleTypeDeclaration TkComma IdType
                               | TkId TkTwoPoints IdType'''
    if (len(p) == 6):
        p[0] = Node("Ident", p[1], [p[3]])
    else:
        p[0] = Node("Ident", p[1])

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

def p_Instructions(p):
    '''Instructions : InstructionLine InstSequence
                    | InstructionLine'''

    if (len(p) == 3):
        p[0] = [p[1], p[2]]
    else:
        p[0] = [p[1]]


def p_InstSequence(p):
    '''InstSequence : TkSemicolon InstructionLine InstSequence
                    | TkSemicolon InstructionLine'''
    if (len(p) == 4):
        p[0] = Node("InstSequence", "Sequence", [p[2],p[3]])
    else:
        p[0] = Node("InstSequence", "Sequence", [p[2]])

def p_InstructionLine(p):
    '''InstructionLine : Asig
                       | If
                       '''
    p[0] = p[1]

def p_Asig(p):
    '''Asig : TkId TkAsig Expression'''
    p[0] = Node("Asig", "Asig", [Node("Ident", p[1]), p[3]])

def p_If(p):
    '''If : TkIf Guard TkArrow IfContent TkFi'''
    p[0] = Node("If", "If", [p[2], p[4]])

def p_Guard(p):
    '''Guard : Expression'''
    p[0] = Node("Guard", "Guard", p[1])

def p_IfContent(p):
    '''IfContent : TkOBracket TkCBracket Guard TkArrow IfContent
          | ProgramBlock
          | Instructions'''

#def p_For(p):
#    '''For : TkFor In TkArrow ProgramBlock TkRof'''
#    p[0] = Node("For", "For", [p[2], p[4]])

#def p_In(p):
#    '''In : TkId TkIn Expresion TkTo Expresion'''
#    p[0] = Node("In", "In", [p[1], p[3], p[5]])
    
def p_Expression(p):
    '''Expression : ExpInt'''
    p[0] = Node("Expression", "Exp", [p[1]])

def p_ExpInt(p):
    '''ExpInt : ExpInt TkPlus ExpInt
              | ExpInt TkMinus ExpInt
              | ExpInt TkMult ExpInt
              | ExpInt TkDiv ExpInt
              | ExpInt TkMod ExpInt
              | TkOpenPar ExpInt TkClosePar
              | IntValue'''
    if p[1] != '(':
        if len(p) > 2:
            if p[2] == '+':
                p[0] = Node("BinOp", "Plus", [p[1], p[3]])
            elif p[2] == '-':
                p[0] = Node("BinOp", "Minus", [p[1], p[3]])
            elif p[2] == '*':
                p[0] = Node("BinOp", "Mult", [p[1], p[3]])
            elif p[2] == '/':
                p[0] = Node("BinOp", "Div", [p[1], p[3]])
            elif p[2] == '%':
                p[0] = Node("BinOp", "Mod", [p[1], p[3]])
            else:
                p_error(p[2])
        else:
            p[0] = p[1]
    else:
        p[0] = p[2]


def p_IntValue(p):
    '''IntValue : TkMinus AbsValue
                | AbsValue'''
    if len(p) == 3:
        p[0] = Node("IntValue", "UnaryMinus", [p[2]])
    else:
        p[0] = p[1]

def p_AbsValue(p):
    '''AbsValue : TkNum
                | TkId'''

    if type(p[1] is int):
        p[0] = Node("Literal", p[1])
    else:
        p[0] = Node("Ident", p[1])

def p_error(p):
    print("Syntax error in input:")
    print(p)
    print("En la linea: " + str(p.lineno))
    sys.exit()


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
newLexer = CustomLexer()
newLexer.build()
tokens = newLexer.tokens
precedence = (
    ('left', 'TkTwoPoints'),
    ('right', 'TkAsig'),
    ('nonassoc', 'TkEqual', 'TkNequal'),
    ('left', 'TkLess', 'TkLeq', 'TkGeq', 'TkGreater'),
    ('left', 'TkPlus', 'TkMinus'), 
    ('left', 'TkMult', 'TkDiv', 'TkMod'))
parser = yacc.yacc()

with open(sys.argv[1]) as fp:
    parser.parse(fp.read(), lexer = newLexer.lexer)
fp.closed