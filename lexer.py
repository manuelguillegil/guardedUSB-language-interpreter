##Proyecto Traductores e Interpretadores, CI-3725
##Entrega 1
##Manuel Gil, 14-10397
##Diego Peña, 15-11095
##Fecha de inicio: 28-09-2019, 19:44 Hora de Venezuela
##Fecha de modificación: 29-09-2019, 10:59 Hora de Venezuela

#Comentarios generales: Antlr es muy complicado para aprender en una semana. Viva Python y Ply

#Últimas modificaciones: Eliminé de palabras reservadas unas cosas que cuentan como tokens, y otras que no estaban en la
#especificación de GuardedUSB. Acomodé t_TkId() para que distinga entre palabras reservadas de identificadores. También
#revisé el mensaje de error porque daba el número de línea con lexpos y es con lineno. Errores de tipeo

#To Do: 
# Falta añadir en que columna se produjo el error en la función de t_error.
# Fala añadir el número de filas y columnas en el print del token (Formatear output). 
# Faltan varias palabras reservadas en la lista
# Hay un error en la función de error, por eso la comenté, pero hay que ver que es y arreglarlo
# Falta hacer que lea el input de un archivo directamente

#Esto es lo que me dice un video en internet que debo importar, pero no se cuales hagan falta al final
import ply.lex as lex #Luthor
import re
import codecs
import sys
import os

tokens = ['TkOBlock', 'TkCBlock', 'TkSoForth', 'TkComma', 'TkOpenPar', 'TkClosePar', 'TkAsig', 
        'TkSemicolon', 'TkArrow', 'TkPlus', 'TkMinus', 'TkMult', 'TkDiv', 'TkMod', 'TkOr', 
        'TkAnd', 'TkNot', 'TkLess', 'TkLeq', 'TkGeq', 'TkGreater', 'TkEqual', 'TkNequal', 
        'TkOBracket', 'TkCBracket', 'TkTwoPoints', 'TkConcat', 'TkNum', 'TkId']

reservadas = {
    'if':   'TkIf',
    'fi':   'TkFi',
    'do':   'TkDo',
    'od':   'TkOd',
    'bool': 'TkBool',
    'int':  'TkInt',
    'array':'TkArray'
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

def t_TkNum(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_TkId(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reservadas.get(t.value,'TkId') 
    return t

# El lexer identifica los comentarios, pero no hace nada ya que no es necesario guardar el token
def t_COMMENT(t):
    r'//.*'
    pass

# Calcular columna. 
# input es la cadena de texto de entrada 
# token es una instancia de token 
def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

# Regla para que podamos rastrear los números de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

#Función cuando existe un error en el token
def t_error(t):
    #print("Error: Unexpected character " + str(t.value[0]) + "in row " + str(t.lineno]) +  ", column ")
    t.lexer.skip (1)


############## MAIN #################### Deberíamos ponerlo en otro archivo

# Construir el lexer
lexer = lex.lex()

# Hacer un input al lexer
lexer.input("int x := 5; if x == 5 --> x := 6; fi")

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)