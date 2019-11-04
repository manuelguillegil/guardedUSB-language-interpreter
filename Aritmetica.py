from CustomLexer import CustomLexer
from AST import Node
import ply.yacc as yacc
import sys

def p_ProgramBlock(p):
    '''ProgramBlock : TkOBlock  Instructions TkCBlock'''
    p[0] = Node("ProgramBlock", "Block", p[2])
    p[0].printTree("")


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
    '''InstructionLine : Asig'''
    p[0] = p[1]

def p_Asig(p):
    '''Asig : TkId TkAsig Expression'''
    p[0] = Node("Asig", "Asig", [Node("Ident", p[1]), p[3]])

def p_Expression(p):
    '''Expression : ExpAux'''
    p[0] = Node("Expression", "Exp", [p[1]])

def p_ExpAux(p):
    '''ExpAux  : ExpAux TkEqual ExpAux
               | ExpAux TkNequal ExpAux
               | ExpAux TkGeq ExpAux
               | ExpAux TkGreater ExpAux
               | ExpAux TkLeq ExpAux
               | ExpAux TkLess ExpAux
               | ExpAux TkOr ExpAux
               | ExpAux TkAnd ExpAux
               | ExpAux TkPlus ExpAux
               | ExpAux TkMinus ExpAux
               | ExpAux TkMult ExpAux
               | ExpAux TkDiv ExpAux
               | ExpAux TkMod ExpAux
               | TkOpenPar ExpAux TkClosePar
               | ExpAux TkComma ExpAux
               | ExpAux TkOBracket ExpAux TkCBracket
               | ExpAux TkOpenPar ExpAux TkTwoPoints ExpAux TkClosePar
               | TkNot ExpAux
               | Value'''
    if p[1] != '(':
        if len(p) == 4:
            if p[2] == '==':
                p[0] = Node("BinOp", "Equals", [p[1], p[3]])
            elif p[2] == '!=':
                p[0] = Node("BinOp", "Nequals", [p[1], p[3]])
            elif p[2] == '!=':
                p[0] = Node("BinOp", "Nequals", [p[1], p[3]])
            elif p[2] == '>=':
                p[0] = Node("BinOp", "Geq", [p[1], p[3]])
            elif p[2] == '>':
                p[0] = Node('BinOp', "Greater", [p[1], p[3]])
            elif p[2] == '<=':
                p[0] = Node("BinOp", "Leq", [p[1], p[3]])
            elif p[2] == '<':
                p[0] == Node('BinOp', "Less", [p[1], p[3]])
            elif p[2] == '\\/':
                p[0] = Node("BinOp", "Or", [p[1], p[3]])
            elif p[2] == '/\\':
                p[0] = Node("BinOp", "And", [p[1], p[3]])
            elif p[2] == '+':
                p[0] = Node("BinOp", "Plus", [p[1], p[3]])
            elif p[2] == '-':
                p[0] = Node("BinOp", "Minus", [p[1], p[3]])
            elif p[2] == '*':
                p[0] = Node("BinOp", "Mult", [p[1], p[3]])
            elif p[2] == '/':
                p[0] = Node("BinOp", "Div", [p[1], p[3]])
            elif p[2] == '%':
                p[0] = Node("BinOp", "Mod", [p[1], p[3]])
            elif p[2] == ',':
                p[0] = Node("ArrayOp", "ArrElementInit", [p[1], p[3]])
            else:
                p_error(p[2])
        elif len(p) == 5:
            p[0] = Node("ArrayOp", "Consult", [p[1], p[3]])
        elif len(p) == 7:
            p[0] = Node("ArrayOp", "ArrayAsig", [p[1], p[3], p[5]])
        elif len(p) == 3:
            p[0] = Node("UnOp", "Not", [p[2]])
        else:
            p[0] = p[1]
    else:
        p[0] = p[2]


def p_Value(p):
    '''Value : TkMinus AbsValue
             | TkMinus Function
             | AbsValue
             | Function'''
    if len(p) == 3:
        p[0] = Node("Value", "UnaryMinus", [p[2]])
    else:
        p[0] = p[1]

def p_Function(p):
    '''Function : TkAtoi TkOpenPar AbsValue TkClosePar
                | TkSize TkOpenPar AbsValue TkClosePar
                | TkMax TkOpenPar AbsValue TkClosePar
                | TkMin TkOpenPar AbsValue TkClosePar'''
    p[0] = Node("Function", p[1], [p[3]])

def p_AbsValue(p):
    '''AbsValue : TkNum
                | TkId
                | TkTrue
                | TkFalse'''

    if type(p[1]) is int:
        p[0] = Node("Literal", p[1])
    else:
        if p[1] == 'true' or p[1] == 'false':
            p[0] = Node("Literal", p[1])
        else:
            p[0] = Node("Ident", p[1])

def p_error(p):
    print("Syntax error in input")
    print(p)
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
precedence = (('left', 'TkTwoPoints'), ('left', 'TkEqual', 'TkNequal'), 
             ('nonassoc', 'TkGeq', 'TkGreater', 'TkLeq', 'TkLess'), ('right', 'TkComma'), ('left', 'TkOBracket'),
             ('left', 'TkPlus', 'TkMinus'), ('left', 'TkMult', 'TkDiv', 'TkMod'), 
             ('left', 'TkOr'), ('left', 'TkAnd'), ('right', 'TkNot'))
parser = yacc.yacc()

with open(sys.argv[1]) as fp:
    parser.parse(fp.read(), lexer = newLexer.lexer)
fp.closed