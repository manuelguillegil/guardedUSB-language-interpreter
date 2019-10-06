##Proyecto Traductores e Interpretadores, CI-3725
##Entrega 1
##Manuel Gil, 14-10397
##Diego Peña, 15-11095
##Fecha de inicio: 28-09-2019, 19:44 Hora de Venezuela
##Fecha de modificación: 05-10-2019, 19:31 Hora de Venezuela

#Comentarios generales: Antlr es muy complicado para aprender en una semana. Viva Python y Ply

#Últimas modificaciones: Ya lee el input de un archivo. Calcula correctamente el número de columna en un caso
#de output normal siempre y cuando no haya tabs en las líneas. Da error si no tiene archivo de input o si este no
#tiene extensión .gusb. Ya da mensajes de error

#Bugs
#No da bien el número de columnas cuando hay tabs

#To Do: 
# Arreglar el bug

## Este programa solo funciona con Python3
import ply.lex as lex #Luthor
import re
import sys
import os #No se si esta va

class CustomLexer(object):

    errors = 0

    tokens = ['TkOBlock', 'TkCBlock', 'TkSoForth', 'TkComma', 'TkOpenPar', 'TkClosePar', 'TkAsig', 
            'TkSemicolon', 'TkArrow', 'TkPlus', 'TkMinus', 'TkMult', 'TkDiv', 'TkMod', 'TkOr', 
            'TkAnd', 'TkNot', 'TkLess', 'TkLeq', 'TkGeq', 'TkGreater', 'TkEqual', 'TkNequal', 
            'TkOBracket', 'TkCBracket', 'TkTwoPoints', 'TkConcat', 'TkIdError', 'TkNum', 'TkId']

    reservadas = {
        'if':   'TkIf',
        'fi':   'TkFi',
        'do':   'TkDo',
        'od':   'TkOd',
        'bool': 'TkBool',
        'int':  'TkInt',
        'array':'TkArray',
        'declare':'TkDeclare',
        'println':'TkPrintln',
        'print':'TkPrint',
        'for':'TkFor',
        'in':'TkIn',
        'to':'TkTo',
        'rof':'TkRof',
        'read':'Tkread',
        'count':'TkCount',
        'atoi':'TkAtoi',
        'size':'TkSize',
        'max':'TkMax',
        'min':'TkMin'
    }
    
    # Una cadena que contiene caracteres ignorados (espacios y tabulaciones) 
    t_ignore = ' \t' 
    t_TkOBlock = r'\|\['
    t_TkCBlock = r'\]\|'
    t_TkSoForth = r'\.\.'
    t_TkComma = r','
    t_TkOpenPar = r'\('
    t_TkClosePar = r'\)'
    t_TkAsig = r':='
    t_TkSemicolon = r';'
    t_TkArrow = r'\-\->'
    t_TkPlus = r'\+'
    t_TkMinus = r'\-'
    t_TkMult = r'\*'
    t_TkDiv = r'/'
    t_TkMod = r'%'
    t_TkOr = r'\\/'
    t_TkAnd = r'/\\'
    t_TkNot = r'!'
    t_TkLess = r'<'
    t_TkLeq = r'<='
    t_TkGeq = r'>='
    t_TkGreater = r'>'
    t_TkEqual = r'=='
    t_TkNequal = r'!='
    t_TkOBracket = r'\['
    t_TkCBracket = r'\]'
    t_TkTwoPoints = r':'
    t_TkConcat = r'\|\|'

    # Concatenamos los tokens y las palabras reservadas
    tokens = tokens + list(reservadas.values())

    def t_TkIdError(self, t):
        r'\d+[a-zA-Z_][a-zA-Z0-9_]*'
        self.t_error(t)


    def t_TkNum(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_TkId(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = self.reservadas.get(t.value,'TkId') 
        return t

    # El lexer identifica los comentarios, pero no hace nada ya que no es necesario guardar el token
    def t_COMMENT(self, t):
        r'//.*'
        pass

    # token es una instancia de token tal que queremos calcular la lexpos donde empieza la línea de ese token
    # start es el lexpos donde empezaba la línea anterior a la de este token
    # return: La lexpos donde empieza la línea que contiene al token
    def find_line_start(self, token, start):
        line_start = self.lexer.lexdata.rfind('\n', start, token.lexpos) + 1
        return line_start

    def find_line(self, t):
        t.lexer.lineno += t.value.count('\n')
        return t.lexer.lineno

    # Regla para que podamos rastrear los números de línea
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    #Función cuando existe un error en el token
    def t_error(self, t):
        col = t.lexpos - self.find_line_start(t, 0) + 1
        print("Error: Unexpected character " + str(t.value[0]) + " in row " + str(t.lineno) +  ", column " + str(col))
        self.errors += 1
        t.lexer.skip (1)

    def build(self,**kwargs):
         self.lexer = lex.lex(module=self, **kwargs)

    def analysis(self, text):
        self.lexer.input(text)

        #prevLine guarda el número de la última línea leída
        #lineStart representa la lexpos donde empieza la línea del token que estamos imprimiendo. Al inicio está en cero
        #porque esa es la menor lexpos posible
        prevLine = 0
        lineStart = 0
        output = ""

        while True:

            tok = self.lexer.token()
            
            if not tok: 
                break

            #Si la última línea leída es distinta de la actual, cambiamos de línea y hay que calcular donde
            #empieza esta nueva línea para determinar la columna de los tokens en esta nueva línea
            if prevLine != tok.lineno:
                lineStart = self.find_line_start(tok, lineStart)
                prevLine = tok.lineno

            #Usando la lexpos del token actual y la lexpos donde comienza la línea, obtenemos la columna del token
            col = tok.lexpos - lineStart + 1

            if tok.type == 'TkId':
                output += '%s(%r) %d %d\n' % (tok.type, tok.value, tok.lineno, col)
            elif tok.type == 'TkNum':
                output += '%s("%r") %d %d\n' % (tok.type, tok.value, tok.lineno, col)
            else:
                output += '%s %d %d\n' % (tok.type, tok.lineno, col)

        if self.errors > 0:
            print("Total errors: " + str(self.errors))
        else:
            print(output)

############## MAIN #################### Deberíamos ponerlo en otro archivo

#Nos aseguramos de que haya un arcghivo de input
try:
    assert(len(sys.argv) > 1)
except:
    print("No hay archivo de input")
    sys.exit()

#Nos aseguramos de que el archivo input tenga la extensión requerida
try:
    assert('.gusb' in sys.argv[1])
except:
    print("Este tipo de archivo no es reconocido")
    sys.exit()

# Construir el lexer
lexer = CustomLexer()
lexer.build()

with open(sys.argv[1]) as fp:
    lexer.analysis(fp.read())
fp.closed

