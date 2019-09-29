##Proyecto Traductores e Interpretadores, CI-3725
##Entrega 1
##Manuel Gil, 14-10397
##Diego Peña, 15-11095
##Fecha de inicio: 28-09-2019, 19:44 Hora de Venezuela
##Fecha de modificación: 28-09-2019, 21:32 Hora de Venezuela

#Comentarios generales: Antlr es muy complicado para aprender en una semana. Viva Python y Ply

#Últimas modificaciones: Creación de los tokens para operadores, paréntesis, brackets, etc. así como
#números e identificadores

#To Do: La función para identificar t_TkId, las palabras reservadas. Probar si los tokens escritos funcionan

#Esto es lo que me dice un video en internet que debo importar, pero no se cuales hagan falta al final
import ply.lex as lex #Luthor
import re
import codecs
import sys
import os

tokens = ['TkOBlock', 'TkCBlock', 'TkSoForth', 'TkComma', 'TkOpenPar', 'TkClosePar', 'TkAsig', 'TkSemicolon', 
        'TkArrow', 'TkPLus', 'TkMinus', 'TkMult', 'TkDiv', 'TkMod', 'TkOr', 'TkAnd', 'TkNot', 'TkLess', 'TkLeq', 
        'TkGeq', 'TkGreater', 'TkEqual', 'TkNequal', 'TkOBracket', 'TkCBracket', 'TkTwoPoints', 
        'TkConcat', 'TkNum', 'TkId']

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

def t_TkNum(t):
    r'\d+'
    t.value = int(t.value)
    return t

