##Proyecto Traductores e Interpretadores, CI-3725
##Entrega 1
##Manuel Gil, 14-10397
##Diego Peña, 15-11095
##Fecha de inicio: 28-09-2019, 19:44 Hora de Venezuela
##Fecha de modificación: 07-09-2019 17:32

#Últimas modificaciones: Ya solucionamos el problema de que ply leía un tab como un solo caracter y por eso calculaba
#mal las columnas. Sin embargo, trabajamos asumiendo que un tab = 4 espacios. Arreglé un error que cuando iba a revisar
#l extensión del archivo

## Este programa solo funciona con Python3
import ply.lex as lex #Luthor
import re
import sys

#Este lexer se basa en el tutorial que se encuentra en la documentación oficial de ply
#http://www.dabeaz.com/ply/ply.html#ply_nn17

#El lexer se trabaja dentro de una clase porque así era más fácil llevar la cuenta de los errores encontrados,
#lo cual era necesario para determinar la información que se debía imprimir al final del análisis 

class CustomLexer(object):

    #Este es un atributo de la clase que permite llevar la cuenta de los errores lexicográficos encontrados
    #ES necesario que exista, porque así la función de manejador de error puede determinar cuantos errores hay
    #de una manera mucho más sencilla de entender para el lector
    errors = 0

    tokens = ['TkOBlock', 'TkCBlock', 'TkSoForth', 'TkComma', 'TkOpenPar', 'TkClosePar', 'TkAsig', 
            'TkSemicolon', 'TkArrow', 'TkPlus', 'TkMinus', 'TkMult', 'TkDiv', 'TkMod', 'TkOr', 
            'TkAnd', 'TkNot', 'TkLess', 'TkLeq', 'TkGeq', 'TkGreater', 'TkEqual', 'TkNequal', 
            'TkOBracket', 'TkCBracket', 'TkTwoPoints', 'TkConcat', 'TkNum', 'TkId', 'TkQuote', 'TkDoubleQuote', 'TkSpace']

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
        'min':'TkMin',
    }
    
    # Una cadena que contiene caracteres ignorados (espacios y tabulaciones) 
    t_ignore = ' \t'
    t_TkOBlock = r'\|\['
    t_TkCBlock = r'\]\|'
    t_TkSoForth = r'\.\.'
    t_TkSpace = r'\\n'
    t_TkComma = r','
    t_TkOr = r'\\/'
    t_TkAnd = r'/\\'
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
    t_TkQuote = r'\''
    t_TkDoubleQuote = r'\"'

    # Concatenamos los tokens y las palabras reservadas
    tokens = tokens + list(reservadas.values())

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

    #Utiliza la lexpos donde inicia la línea del token actual para calcular la columna  del mismo
    #asume tab = 4 espacios
    def find_tok_column(self, lineStart, token):
        last_cr = lineStart - 1
        tab = self.lexer.lexdata.rfind('\t', last_cr, token.lexpos)
        cantidad_tabs = tab - last_cr
        if (cantidad_tabs > 0):
            token.lexpos = token.lexpos + (cantidad_tabs * 2)
            pos = token.lexpos - last_cr
        else:
            pos = token.lexpos - last_cr -1
        if last_cr < 0:
            last_cr = 0
        return pos

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

    #Esta función permite construir el lexer representado por el atributo self.lexer
    def build(self):
         self.lexer = lex.lex(module=self)

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
            col = self.find_tok_column(lineStart, tok) + 1

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

# Construir el lexer
lexer = CustomLexer()
lexer.build()

with open(sys.argv[1]) as fp:
    lexer.analysis(fp.read())
fp.closed

