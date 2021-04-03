import ply.yacc as yacc
import os
import codecs
import re
from lex import tokens
from sys import stdin

#SE PRIORIDAD DE OPERADORES
precedencia = (
    ('nonassoc','SEMIC'),
    ('right','ASSIGN'),
    ('left','NE_LOG'),
    ('nonassoc', 'LT_LOG','LTE_LOG','GTE_LOG','GTE_LOG'),
    ('left', 'PLUS_OP','MINUS_OP'),
    ('left', 'MULT_OP', 'DIV_OP'),
    ('left', 'LPAREN','RPAREN'),
    ('left', 'LBRACK', 'RBRACK'),
    ('left', 'LCURLY', 'RCURLY')
)

#INICIO
def p_programa(p):
    'programa : PROGRAMA ID SEMIC variables funciones bloque'

def p_variables(p):
    '''
    variables : var_aux
              | empty
    '''

def p_var_aux(p):
    '''
    var_aux : VARIABLES var_aux2 
    '''

def p_var_aux2(p):
    '''
    var_aux2 : ID arreglo var_aux3
             | empty
    '''

def p_var_aux3(p):
    '''
    var_aux3 : COMMA var_aux2
             | COLON tipo SEMIC
    '''

def p_arreglo(p):
    '''
    arreglo : LBRACKET INT_CTE arreglo_aux RBRACK p_var_aux3
    '''

def p_arreglo(p):
    '''
    arreglo_aux : COMMA INT_CTE p_arreglo
                | empty
    '''

def p_tipo(p):
    '''
    tipo : INT
         | CHAR
         | FLOAT
    '''

def p_tipo_func(p):
    '''
    tipo_func : VOID
              | PRINCIPAL
              | tipo
    '''

def p_funciones(p):
    '''
    funciones : tipo_func  FUNCION ID LPAREN var_aux3 RPAREN SEMIC p_var_aux BLOQUE
              | empty

    '''

def p_bloque(p):
    '''
    bloque : LCURLY estatuto RCURLY
    '''

def p_estatuto(p):
    '''
    estatuto : asignacion
             | condicion
             | loop
             | llamada_funcion
             | escritura
             | lectura
             | llamada_funcion_void
             | empty
    '''


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