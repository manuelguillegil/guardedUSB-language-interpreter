##Proyecto Traductores e Interpretadores, CI-3725
##Entrega 2
##Manuel Gil, 14-10397
##Diego Peña, 15-11095
##Fecha de inicio: 28-09-2019, 00:07 Hora de Venezuela
##Fecha de modificación: 03-11-2019, 21:54 Hora de Venezuela

#Actualización: Desaparecí los conflictos pero ahora o funciona el if o la consulta de arreglos.
#Voy a ver si mañana puedo cambiar eso sin joder todo

from CustomLexer import CustomLexer
from AST import Node, DecNode
import ply.yacc as yacc
import re
import sys

def p_ProgramBlock(p):
    '''ProgramBlock : TkOBlock TkDeclare DeclareLines Instructions TkCBlock
                    | TkOBlock Instructions TkCBlock'''
    #print("Regla1")
    if len(p) == 6:
        p[0] = Node("ProgramBlock", "Block", [Node("Declare", "Declare", [p[3]])] + p[4])
    else:
        p[0] = Node("ProgramBlock", "Block", p[2])
        #print(len(p[0].children))
    p[0].printTree("")

def p_DeclareLines(p):
    '''DeclareLines : DeclareLines VarDeclaration
                    | VarDeclaration'''
    #print("Regla3")
    if(len(p) == 3):
        SequenceChild = DecNode("DeclarationLine", "DeclarationLine", p[2])
        p[1].addChildren([Node('Sequence', 'Sequence', [SequenceChild])])
        p[0] = p[1]
    else:
        #p[1]contiene una lista de variables declaradas en esa línea
        p[0] = DecNode("DeclarationLine", "DeclarationLine", p[1], True)

def p_VarDeclaration(p):
    '''VarDeclaration : MultipleTypeDeclaration TkSemicolon
                      | SingleTypeDeclaration'''
#| SingleTypeDeclaration
    #print("Regla5")
    p[0] = p[1]

def p_MultipleTypeDeclaration(p):
    '''MultipleTypeDeclaration : TkId TkComma MultipleTypeDeclaration TkComma IdType
                               | TkId TkTwoPoints IdType'''
    #print("Regla6")
    if (len(p) == 6):
        p[0] = [Node("Ident", p[1])] + p[3]
    else:
        p[0] = [Node("Ident", p[1])]

def p_SingleTypeDeclaration(p):
    '''SingleTypeDeclaration : TkId TkComma SingleTypeDeclaration
                             | TkId TkComma TkId TkTwoPoints IdType TkSemicolon'''
    if len(p) == 4:
        p[0] = [Node("Ident", p[1])] + p[3]
    else:
        p[0] = [Node("Ident", p[1]), Node("Ident", p[3])]

def p_IdList(p):
    '''IdList : IdList TkId TkComma
              | TkId TkComma'''
    print("Regla8")
    if(len(p) == 4):
        p[1].append(Node('Ident', p[2]))
        p[0] = p[1]
    else:
        p[0] = [Node("Ident", p[1])]
        print(p[0])

def p_IdType(p):
    '''IdType : TkInt
              | TkBool
              | TkArray TkOBracket TkNum TkSoForth TkNum TkCBracket'''
    #print("Regla9")

def p_Instructions(p):
    '''Instructions : InstructionLine InstSequence
                    | InstructionLine'''
    #print("Regla10")

    if (len(p) == 3):
        p[0] = [p[1], p[2]]
    else:
        p[0] = [p[1]]

def p_InstSequence(p):
    '''InstSequence : TkSemicolon InstructionLine InstSequence
                    | TkSemicolon InstructionLine'''
    #print("Regla11")
    if (len(p) == 4):
        p[0] = Node("InstSequence", "Sequence", [p[2],p[3]])
    else:
        p[0] = Node("InstSequence", "Sequence", [p[2]])

def p_InstructionLine(p):
    '''InstructionLine : Asig
                       | IfDo
                       | Println
                       | Print
                       | For
                       '''
    #print("Regla12")
    p[0] = p[1]

def p_Asig(p):
    '''Asig : TkId TkAsig ExpAux'''
    #print("Regla13")
    p[0] = Node("Asig", "Asig", [Node("Ident", p[1]), Node("Exp", "Exp", [p[3]])])

def p_IfDo(p):
    '''IfDo : TkIf Body TkFi
            | TkDo Body TkOd'''
    #print("Regla14")
    p[0] = Node(p[1], p[1], [p[2]])

<<<<<<< HEAD
# def p_Println(p):
#     '''Println : TkPrintln ExpAux TkSemicolon
#                | TkPrintln TkId TkSemicolon'''
#     #print("Regla15")
#     p[0] = Node("Println", "Println", [Node("Exp", "Exp", [p[2]])])

# def p_Print(p):
#     '''Print : TkPrint ExpAux TkSemicolon
#              | TkPrint TkId TkSemicolon'''
#     #print("Regla16")
#     p[0] = Node("Print", "Print", [Node("Exp", "Exp", [p[2]])])
=======
def p_Println(p):
    '''Println : TkPrintln ExpAux
               | TkPrintln TkString TkConcat Concat
               | TkPrintln ExpAux TkConcat Concat
               | TkPrintln TkString'''
    #print("Regla15")
    if p[2] == 'ExpAux':
        p[0] = Node("Println", "Println", [Node("Exp", "Exp", [p[2]])])
    elif len(p) > 3 and isinstance(p[2], str):
        p[0] = Node("Println", "Println", [Node("String", p[2]) , Node("Concat", "Concat", [p[4]])])
    elif len(p) > 3 and not  isinstance(p[2], str):
        p[0] = Node("Println", "Println", [Node("Exp", "Exp", [p[2]]) , Node("Concat", "Concat", [p[4]])])
    else:
        p[0] = Node("Println", "Println", [Node("String", p[2])])

def p_Print(p):
    '''Print : TkPrint ExpAux
               | TkPrint TkString TkConcat Concat
               | TkPrint ExpAux TkConcat Concat
               | TkPrint TkString'''
    if p[2] == 'ExpAux':
        p[0] = Node("Print", "Print", [Node("Exp", "Exp", [p[2]])])
    elif len(p) > 3 and isinstance(p[2], str):
        p[0] = Node("Print", "Print", [Node("String", p[2]) , Node("Concat", "Concat", [p[4]])])
    elif len(p) > 3 and not  isinstance(p[2], str):
        p[0] = Node("Print", "Print", [Node("Exp", "Exp", [p[2]]) , Node("Concat", "Concat", [p[4]])])
    else:
        p[0] = Node("Print", "Print", [Node("String", p[2])])

def p_Concat(p):
    '''Concat : TkString TkConcat Concat
               | ExpAux TkConcat Concat
               | TkString
               | ExpAux'''
    if len(p) > 3 and not isinstance(p[1], str):
        p[0] = Node("Concat", "Concat", [Node("Exp", "Exp", [p[1]]) , Node("Concat", "Concat", [p[3]])])
    elif len(p) > 3 and isinstance(p[1], str):
        p[0] = Node("Concat", "Concat", [Node("String", p[1]) , Node("Concat", "Concat", [p[3]])])
    elif len(p) < 3 and isinstance(p[1], str):
        p[0] = Node("String", p[1])
    elif len(p) < 3 and not isinstance(p[1], str):
        p[0] = Node("Exp", "Exp", [p[1]])
    else:
        pass
>>>>>>> d66a58489142c6b4ccdfcc44f0e89de0d84b6da5

def p_Body(p):
    '''Body : ExpAux TkArrow Instructions GuardList
            | ExpAux TkArrow Instructions'''
    #print("Regla15")
    if len(p) == 5:
        p[0] = Node("Guard", "Guard", [Node("Exp", "Exp", [p[1]])] + p[3] + [p[4]])
    else:
        p[0] = Node("Guard", "Guard", [Node("Exp", "Exp", [p[1]])] + p[3])


def p_GuardList(p):
    '''GuardList : TkGuard ExpAux TkArrow Instructions GuardList
                 | TkGuard ExpAux TkArrow Instructions'''
    #print("Regla16")
    if len(p) == 7:
        p[0] = Node("Guard", "Guard", [Node("Exp", "Exp", [p[2]])] + p[4] + [p[5]])
    else:
        p[0] = Node("Guard", "Guard", [Node("Exp", "Exp", [p[2]])] + p[4])


def p_For(p):
    '''For : TkFor In TkArrow Instructions TkRof'''
    p[0] = Node("For", "For", [Node("In", "In",  [p[2]]), Node("Block", "Block",  p[4])  ])

def p_In(p):
    '''In : TkId TkIn ExpAux TkTo ExpAux'''
    p[0] = Node("Ident", p[1], [p[3], p[5]])

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
    #print("Regla17")
    #print(p[1].value)
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
            #print("Last")
            p[0] = p[1]
    else:
        p[0] = p[2]


def p_Value(p):
    '''Value : TkMinus AbsValue
             | TkMinus Function
             | AbsValue
             | Function'''
    #print("Regla18")
    if len(p) == 3:
        p[0] = Node("Value", "UnaryMinus", [p[2]])
    else:
        p[0] = p[1]

def p_Function(p):
    '''Function : TkAtoi TkOpenPar AbsValue TkClosePar
                | TkSize TkOpenPar AbsValue TkClosePar
                | TkMax TkOpenPar AbsValue TkClosePar
                | TkMin TkOpenPar AbsValue TkClosePar'''
    #print("Regla19")
    p[0] = Node("Function", p[1], [p[3]])

def p_AbsValue(p):
    '''AbsValue : TkNum
                | TkId
                | TkTrue
                | TkFalse'''
    #print("Regla20")
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
precedence = (
    #('left', 'TkSemicolon'),
    #('left', 'TkPrintln', 'TkPrint'),
    #('left', 'TkOBracket', 'TkCBracket'),
    ('left', 'TkTwoPoints'),
    #('left', 'TkId', 'TkInt', 'TkBool', 'TkArray'),
    #('right', 'TkAsig'),
    ('left', 'TkEqual', 'TkNequal'),
    ('nonassoc', 'TkLess', 'TkLeq', 'TkGeq', 'TkGreater'),
    ('right', 'TkComma'), 
    ('left', 'TkOBracket'), 
    ('left', 'TkPlus', 'TkMinus'), 
    ('left', 'TkMult', 'TkDiv', 'TkMod'),
    ('left', 'TkOr'), ('left', 'TkAnd'), ('right', 'TkNot'))
parser = yacc.yacc()

with open(sys.argv[1]) as fp:
    parser.parse(fp.read(), lexer = newLexer.lexer)
fp.closed