##Proyecto Traductores e Interpretadores, CI-3725
##Entrega 2
##Manuel Gil, 14-10397
##Diego Peña, 15-11095
##Fecha de inicio: 28-09-2019
##Fecha de modificación: 07-11-2019 

#Actualización: YA arreglé el detalle de la gramática

from CustomLexer import CustomLexer
from AST import Node, DecNode, BlockNode, ForNode
import ply.yacc as yacc
import re
import sys

#Var info es una tupla que contiene en el primer elemento la lista de nodos que representan las variables declaradas
# en una determinada línea y la segunda es la lista de tipos que tienen las variables en esa línea 
def generateTupleList(varInfo):
    tupleList = []
    for i in range(len(varInfo[0])):
        if len(varInfo[1]) == 1:
            tupleList.append((varInfo[0][i].getValue(), varInfo[1][0]))
        else:
            tupleList.append((varInfo[0][i].getValue(), varInfo[1][i]))

    return tupleList

def p_Start(p):
    '''Start : ProgramBlock'''
    p[0] = p[1]
    p[0].printTree("")

def p_ProgramBlock(p):
    '''ProgramBlock : TkOBlock TkDeclare DeclareLines Instructions TkCBlock
                    | TkOBlock Instructions TkCBlock'''
    #print("Regla1")
    if len(p) == 6:
        p[0] = BlockNode("ProgramBlock", "Block", [Node("Declare", "Declare", [p[3]])] + p[4], p[3].getDeclaredVars())
    else:
        p[0] = BlockNode("ProgramBlock", "Block", p[2])
        #print(len(p[0].children))

def p_DeclareLines(p):
    '''DeclareLines : DeclareLines TkSemicolon VarDeclaration
                    | VarDeclaration'''
    #print("Regla3")
    if(len(p) == 4):
        tupleList = generateTupleList(p[3])
        SequenceChild = DecNode("DeclarationLine", "DeclarationLine", tupleList, p[3][0])
        p[1].addChildren([Node('Sequence', 'Sequence', [SequenceChild])]) #CAmbiar por addChild, así me enrredo menos
        p[1].addTupleList(SequenceChild.getDeclaredVars())
        p[0] = p[1]
    else:
        tupleList = generateTupleList(p[1])
        p[0] = DecNode("DeclarationLine", "DeclarationLine", tupleList, p[1][0], True)

def p_VarDeclaration(p):
    '''VarDeclaration : MultipleTypeDeclaration
                      | SingleTypeDeclaration'''
#| SingleTypeDeclaration
    #print("Regla5")
    p[0] = p[1]

def p_MultipleTypeDeclaration(p):
    '''MultipleTypeDeclaration : TkId TkComma MultipleTypeDeclaration TkComma IdType
                               | TkId TkTwoPoints IdType'''
    #print("Regla6")
    if (len(p) == 6):
        p[0] = ([Node("Ident", p[1])] + p[3][0], p[5] + p[3][1])
    else:
        p[0] = ([Node("Ident", p[1])], p[3])
        #El caso bse devuelve una tupla que en el primer término contiene el identificador en una lista
        #y en el segundo los tipos de la declaración

def p_SingleTypeDeclaration(p):
    '''SingleTypeDeclaration : TkId TkComma SingleTypeDeclaration
                             | TkId TkComma TkId TkTwoPoints IdType'''
    if len(p) == 4:
        p[0] = ([Node("Ident", p[1])] + p[3][0], p[3][1])
    else:
        p[0] = ([Node("Ident", p[1]), Node("Ident", p[3])], p[5])

def p_IdType(p):
    '''IdType : TkInt
              | TkBool
              | TkArray TkOBracket TkNum TkSoForth TkNum TkCBracket
              | TkArray TkOBracket TkMinus TkNum TkSoForth TkNum TkCBracket
              | TkArray TkOBracket TkMinus TkNum TkSoForth TkMinus TkNum TkCBracket''' 
    #print("Regla9")

    tipo = ""

    for i in range(1, len(p)):
        tipo += str(p[i])
    
    p[0] = [tipo]


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
                       | Printing
                       | For
                       | ProgramBlock
                       | Read
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

def p_Printing(p):
    '''Printing : TkPrintln ExpAux
                | TkPrint ExpAux
                | TkPrintln TkString TkConcat Concat
                | TkPrint TkString TkConcat Concat
                | TkPrintln ExpAux TkConcat Concat
                | TkPrint ExpAux TkConcat Concat
                | TkPrintln TkString
                | TkPrint TkString'''
    #print("Regla15")
    if len(p) == 3:
        if type(p[2]) is str:
            p[0] = Node(p[1], p[1], [Node("String", p[2])])
        else:
            p[0] = Node(p[1], p[1], [Node("Exp", "Exp", [p[2]])])
    else:
        if type(p[2]) is str:
            p[0] = Node(p[1], p[1], [Node("String", p[2]) , Node("Concat", "Concat", [p[4]])])
        else:
            p[0] = Node(p[1], p[1], [Node("Exp", "Exp", [p[2]]) , Node("Concat", "Concat", [p[4]])])

def p_Read(p):
    '''Read : Tkread TkId'''
    p[0] = Node("Read", "Read", [Node("Ident", p[2])])

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
    '''For : TkFor In TkArrow ProgramBlock TkRof'''
    #print("Hey there")
    p[0] = Node("For", "For", [Node("In", "In",  [p[2]]), p[4]])

def p_In(p):
    '''In : TkId TkIn ExpAux TkTo ExpAux'''
    p[0] = ForNode("Ident", p[1], [p[3], p[5]], p[1])

def p_ExpAux(p):
    '''ExpAux  : ExpAux TkOpenPar ExpAux TkTwoPoints ExpAux TkClosePar
               | ExpAux TkEqual ExpAux
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
               | TkMinus TkOpenPar ExpAux TkClosePar
               | ExpAux TkOBracket ExpAux TkCBracket
               | TkAtoi TkOpenPar ExpAux TkClosePar
               | TkSize TkOpenPar ExpAux TkClosePar
               | TkMax TkOpenPar ExpAux TkClosePar
               | TkMin TkOpenPar ExpAux TkClosePar
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
            elif p[2] == '>=':
                p[0] = Node("RelOp", "Geq", [p[1], p[3]])
            elif p[2] == '>':
                p[0] = Node('RelOp', "Greater", [p[1], p[3]])
            elif p[2] == '<=':
                p[0] = Node("RelOp", "Leq", [p[1], p[3]])
            elif p[2] == '<':
                p[0] = Node('RelOp', "Less", [p[1], p[3]])
            elif p[2] == '\\/':
                p[0] = Node("BoolOp", "Or", [p[1], p[3]])
            elif p[2] == '/\\':
                p[0] = Node("BoolOp", "And", [p[1], p[3]])
            elif p[2] == '+':
                p[0] = Node("AritOp", "Plus", [p[1], p[3]])
            elif p[2] == '-':
                p[0] = Node("AritOp", "Minus", [p[1], p[3]])
            elif p[2] == '*':
                p[0] = Node("AritOp", "Mult", [p[1], p[3]])
            elif p[2] == '/':
                p[0] = Node("AritOp", "Div", [p[1], p[3]])
            elif p[2] == '%':
                p[0] = Node("BinOp", "Mod", [p[1], p[3]])
            elif p[2] == ',':
                p[0] = Node("ArrayOp", "ArrElementInit", [p[1], p[3]])
            else:
                p_error(p[2])
        elif len(p) == 5:
            if p[2] == '[':
                p[0] = Node("ArrayOp", "ArrConsult", [p[1], Node("Exp", "Exp", [p[3]])])
            else:
                if p[1] == '-':
                    p[0] = Node("UnaryMinus", "UnaryMinus", [p[3]])
                else:
                    p[0] = Node("Function", p[1], [p[3]])
        elif len(p) == 7:
            p[0] = Node("ArrayOp", "ArrayAsig", [p[1], p[3], p[5]])
        elif len(p) == 3:
            p[0] = Node("BoolOp", "Not", [p[2]])
        else:
            #print("Last")
            p[0] = p[1]
    else:
        p[0] = p[2]


def p_Value(p):
    '''Value : TkMinus AbsValue 
             | AbsValue'''
    #print("Regla18")
    if len(p) == 3:
        p[0] = Node("UnaryMinus", "UnaryMinus", [p[2]])
    else:
        #print(p[1].value)
        p[0] = p[1]

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
    ('left', 'TkOr'), ('left', 'TkAnd'), ('right', 'TkNot'),
    ('nonassoc', 'TkLess', 'TkLeq', 'TkGeq', 'TkGreater'),
    ('right', 'TkComma'), 
    ('left', 'TkOBracket'), 
    ('left', 'TkPlus', 'TkMinus'), 
    ('left', 'TkMult', 'TkDiv', 'TkMod'),
    ('nonassoc', 'TkAtoi', 'TkSize', 'TkMax', 'TkMin'))
parser = yacc.yacc()

with open(sys.argv[1]) as fp:
    parser.parse(fp.read(), lexer = newLexer.lexer)
fp.closed