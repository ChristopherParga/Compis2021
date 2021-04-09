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

# DECLARACION DE ARREGLOS
def p_arreglo(p):
    '''
    arreglo : LBRACKET INT_CTE arreglo_aux RBRACK p_var_aux3
    '''

def p_arreglo_aux(p):
    '''
    arreglo_aux : COMMA INT_CTE p_arreglo
                | empty
    '''

# TIPOS DE VARIABLE Y FUNCIONES
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

# FUNCIONES
def p_funciones(p):
    '''
    funciones : tipo_func FUNCION ID LPAREN var_aux3 RPAREN SEMIC p_var_aux BLOQUE
              | empty

    '''

# BLOQUE
def p_bloque(p):
    '''
    bloque : LCURLY estatuto RCURLY
    '''

# ESTATUTO
def p_estatuto(p):
    '''
    estatuto : asignacion SEMIC
             | condicion SEMIC
             | loop SEMIC
             | llamada_funcion SEMIC
             | escritura SEMIC
             | lectura SEMIC
             | llamada_funcion_void SEMIC
             | empty
    '''

# ASIGNACION
def p_asignacion(p):
    '''
    asignacion : ID arreglo_aux_assign ASSIGN asignacion_aux
    '''

def p_asignacion_aux(p):
    '''
    asignacion_aux : llamada_funcion asignacion_aux2
                   | expresion asignacion_aux2
    '''

def p_asignacion_aux2(p):
    '''
    asignacion_aux2 : expresion asignacion_aux
                    | empty
    '''

# --- Arreglos igual a los de arriba pero con m-exp en lugar de CTE_INT
def p_arreglo_assign_aux(p):
    '''
    arreglo_aux_assign : LBRACK m_exp arreglo_aux_assign2 RBRACK
                       | empty
    '''
def p_arreglo_assign_aux2(p):
    '''
    arreglo_aux_assign2 : COMMA m_exp
                        | empty
    '''

# IF-ELSE
def p_condicion(p):
    '''
    condicion : SI LPAREN expresion RPAREN ENTONCES BLOQUE sino_aux 
    '''

def p_sino_aux(p):
    '''
    sino_aux : SINO bloque
             | empty
    '''

# --- INT_TYPE en lugar de CTE_INT porque puede cambiar(?)
# --- Igual, arreglo_aux_assign porque puede ir una expresion(?)
def p_mientras(p):
    '''
    mientras : MIENTRAS LPAREN expresion RPAREN HACER bloque mientras_aux
             | DESDE ID arreglo_aux_assign ASSIGN INT_TYPE HASTA INT_TYPE HACER bloque desde_aux
    '''
# LOOP
def p_mientras_aux(p):
    '''
    mientras_aux : LPAREN expresion RPAREN HACER bloque mientras_aux
                 | empty
    '''

def p_desde_aux(p):
    '''
    desde_aux : INT_TYPE HASTA INT_TYPE HACER bloque desde_aux
              | empty
    '''

# PARAMETROS
def p_parametros(p):
    '''
    parametros : LPAREN parametros_aux RPAREN
    '''

# --- No estoy seguro si esta la hice bien. Hasta donde sé, da error... pero no se si sea algo que se maneje con los puntos neurargicos.
# --- Lo digo porque segun yo acepta una funcion con un parametro y una coma -> funcion(int 1, ) y no deberia de pasar eso.
def p_parametros_aux(p):
    '''
    parametros_aux : expresion parametros_aux2
                   | empty
    '''

def p_parametros_aux2(p) :
    '''
    parametros_aux2 : COMMA parametrox_aux
                    | empty
    ''' 

# LLAMADA FUNCION
def p_llamada_funcion(p) :
    '''
    llamada_funcion : ID parametros
    '''
# LLMADA FUNCION VOID
def p_llamada_void(p) :
    '''
    llamada_void : ID parametros
    '''

# ESCRITURA
def p_escritura(p) :
    '''
    escritura : ESCRIBE LPAREN escritura_aux RPAREN
    '''
def p_escritura_aux(p) :
    '''
    escritura_aux : STRING_CTE escritura_aux2
                  | expresion escritura_aux2
    '''

def p_escritura_aux2(p) :
    '''
    escritura_aux2 : COMMA escritura_aux
                   | empty
    '''

# LECTURA
def p_lectura(p) : 
    '''
    lectura: LEE LPAREN ASSIGN lectura_aux RPAREN
    '''

def p_lectura_aux(p) :
    '''
    lectura_aux : COMMA ASSIGN lectura_aux
                | empty
    '''

# EXPRESIONES
def p_expresion(p) :
    '''
    expresion : t_exp exp_aux
    '''

def p_exp_aux(p) :
    '''
    exp_aux : OR_LOG expresion
            | empty
    '''

def p_t_exp(p) :
    '''
    t_exp : g_exp t_exp_aux
    '''

def p_t_exp_aux(p) :
    '''
    t_exp_aux : AND_LOG t_exp
              | empty
    '''

def p_g_exp(p) :
    '''
    g_exp : m_exp g_exp_aux
    '''

def p_g_exp_aux(p) :
    '''
    g_exp_aux : LT_LOG m_exp
              | GT_LOG m_exp
              | EQUAL_LOG m_exp
              | NE_LOG m_exp
              | empty
    ''' 

def p_m_exp(p) : 
    '''
    m_exp : termino m_exp_aux
    ''' 

def p_m_exp_aux(p) :
    '''
    m_exp_aux : PLUS_OP m_exp
              | MINUS_OP m_exp
              | empty
    ''' 

def p_termino(p) :
    '''
    termino : factor termino_aux
    '''

def p_termino_aux(p) :
    '''
    termino_aux : MULT_OP termino
                | DIV_OP termino
                | empty
    '''

def p_factor(p) :
    '''
    factor : LPAREN expresion RPAREN
           | p_factor_aux 
           | variables
           | llamada_funcion
    '''

def p_factor_aux(p) :
    '''
    p_factor_aux : INT_CTE
                 | FLOAT_CTE
                 | STRING_CTE
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