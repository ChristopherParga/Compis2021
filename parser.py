import ply.yacc as yacc
import os
import codecs
import re
from lex import tokens
from sys import stdin

parser = yacc.yacc()

def main():
    name = input('File name: ')
    name = "pruebas/" + name + ".txt" 
    print(name)
    try:
        f = open(name,'r', encoding='utf-8')
        result = parser.parse(f.read())
        f.close()
    except EOFError:
        print (EOFError)
main()