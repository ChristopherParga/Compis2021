import ply.yacc as yacc
import os
import codecs
import re
from lexer import tokens, lex_test
from sys import stdin
from DirFunc import *
from CuboSemantico import *

############## FUNCIONES DE LAS PILAS ################

#Te regresa el ultimo elemento de la pila de operandos
def popOperandos():
    global pOperandos
    pop = pOperandos.pop()
    print("--------------------> POP Operandos")
    print("Pop Operandos= ", pop)
    return pop

#Te regresa el ultimo elemento de la pila de operadores
def popOperadores():
    global pOper
    pop = pOper.pop()
    print("--------------------> POP POper")
    print("Pop Poper= ", pop)
    return pop

#Te regresa el ultimo elemento de la pila de tipos
def popTipos():
    global pTipos
    pop = pTipos.pop()
    print("--------------------> POP Tipos")
    print("Pop Tipos = ", pop)
    return pop

#Te regresa el ultimo elemento de la pila de IDs
def popIDs():
    global pIDs
    pop = pIDs.pop()
    print("--------------------> POP IDs")
    print("Pop IDs = ", pop)
    return pop

#Mete a la pila operandos el nuevo ID
def pushIDs(ID):
    global pIDs
    pIDs.append(ID)
    print("------> pushID : ", ID)
    print("PIDs : ", pIDs)

#Mete a la pila operandos el nuevo operando
def pushOperando(operando):
    global pOperandos
    pOperandos.append(operando)
    print("------> pushOperando : ", operando)
    print("POperandos : ", pOperandos)

#Mete a la pila operador el nuevo operador
def pushOperador(operador):
    global pOper
    pOper.append(operador)
    print("------> pushOperador : ", operador)
    print("POper : ", pOper)
    

#Mete a la pila tipos el nuevo tipo
def pushTipo(tipo):
    global pTipos
    pTipos.append(tipo)
    print("------>pushTipo : ", tipo)
    print("pTipos : ", pTipos)

#obtiene el ultimo operando ingresado a la pila de operandos
def topOperador():
    global pOper
    last = len(pOper) - 1
    if (last < 0):
        return 'empty'
    return pOper[last]

#Ultimo tipo ingresado a la pila de tipos
def topTipo():
    global pTipos
    last = len(pTipos) - 1
    if(last < 0):
        return 'empty'
    return pTipos[last]

#Regresa el ultimo elemento de la pila de Saltos
def popSaltos():
    global pSaltos

    return pSaltos.pop()

#Agrega el nuevo salto a la pila de Saltos.
def pushSaltos(salto):
    global pSaltos
    #print("PUSH SALTO: ", salto)
    pSaltos.append(salto)

#Obtiene el indice del siguiente cuadruplo del arreglo de cuadruplos
def nextQuad():
    global cuadruplos
    return len(cuadruplos)

#Regresa el ultimo cuadruplo
def popQuad():
    global cuadruplos
    return cuadruplos.pop()

#Agrega un nuevo cuadruplo al arreglo de cuadruplos
def pushQuad(quad):
    global cuadruplos
    cuadruplos.append(quad)

#Objetos
directorioFunciones = DirFunc()
tablaVariables = TablaVars()
cuboSem = CuboSemantico()

### Pilas para generacion de cuadruplos ####
pOperandos = [] #Pila de operandos pendientes (PilaO)
pOper = [] #Pila de operadores pendientes (POper)
pTipos = [] #Pila de tipos
pSaltos = [] #Pila de saltos para condiciones y ciclos
pFunciones = [] #Pila de funciones
pArgumentos = [] #Pila de agumentos de una funcion
pMemorias = [] # Pila de direcciones de memoria
pDim = [] #Pila de Arreglos
pIDs = [] #Pila de IDs para declaracion

#Arreglo donde se almacenaran todos los cuadruplos que se vayan generando
cuadruplos = []

#Diccionarios de constantes que cuardan la direccion de memoria de constantes
d_ints = {}
d_floats = {}
d_strs = {}
d_ch = {}
d_df = {}

##Constantes
GBL = 'global'
OP_SUMARESTA = ['+', '-']
OP_MULTDIV = ['*', '/']
OP_REL = ['>', '<', '<=', '>=', '==', '!=']
OP_LOGICOS = ['&', '|']
OP_ASIG = ['=']
OP_SECUENCIALES = ['lee', 'escribe', 'regresa']
ESPACIO_MEMORIA = 1000 #Tamano del espacio de memoria

##Variables globales
currentFunc = GBL
currentType = "void"
varName = ""
currentVarName = ""
currentCantParams = 0
currentCantVars = 0
avail = 0
constanteNegativa = False
forBool = False
varFor = ''
negativo = False
returnBool = False #sirve para saber si una funcion debe regresar algun valor (si es void o no)
boolDataf = False #Sirve para saber cuando una variable dataframe esta siendo declarada


#SE PRIORIDAD DE OPERADORES
precedencia = (
    ('nonassoc','SEMIC'),
    ('right','ASSIGN'),
    ('left','NE_LOG'),
    ('nonassoc', 'LT_LOG','LTE_LOG','GT_LOG','GTE_LOG'),
    ('left', 'PLUS_OP','MINUS_OP'),
    ('left', 'MULT_OP', 'DIV_OP'),
    ('left', 'LPAREN','RPAREN'),
    ('left', 'LBRACK', 'RBRACK'),
    ('left', 'LCURLY', 'RCURLY')
)

#INICIO
def p_programa(p):
    '''
    programa : PROGRAMA ID SEMIC dec_variables dec_funciones principal
    '''
    print("PROGRAMA \"", p[2], "\" terminado.")


#Declaracion de Variables
def p_dec_variables(p):
    '''
    dec_variables : VARIABLES dec_variables2
                  | empty
    '''

def p_dec_variables2(p):
    '''
    dec_variables2 : lista_ids COLON tipo pn_AddVariable SEMIC dec_variables3
    '''

def p_dec_variables3(p):
    '''
    dec_variables3 : dec_variables2
                   | empty
    '''

def p_lista_ids(p):
    '''
    lista_ids : ID pn_SaveID DecVarDim lista_ids2
    '''


def p_lista_ids2(p):
    '''
    lista_ids2 : COMMA lista_ids
               | empty
    '''

#Dimensiones
def p_DecVarDim(p):
    '''
    DecVarDim : DecVarDim2
              | empty
    '''

def p_DecVarDim2(p):
    '''
    DecVarDim2 : LBRACK INT_CTE DecVarDim3 RBRACK
    '''

def p_DecVarDim3(p):
    '''
    DecVarDim3 : COMMA INT_CTE
               | empty
    '''

# TIPOS DE VARIABLE
def p_tipo(p):
    '''
    tipo : INT_TYPE pn_SetCurrentType
         | CHAR_TYPE pn_SetCurrentType
         | FLOAT_TYPE pn_SetCurrentType
    '''
    

# Declaracion Funciones
def p_dec_funciones(p):
    '''
    dec_funciones : dec_funciones2 dec_funciones
                  | empty
    '''

def p_dec_funciones2(p):
    '''
    dec_funciones2 : tipo dec_funciones3
                   | VOID pn_SetCurrentType dec_funciones3
    '''

def p_dec_funciones3(p):
    '''
    dec_funciones3 : FUNCION ID pn_AddFunc LPAREN dec_funcion_param RPAREN dec_variables bloque
    '''

def p_dec_funcion_param(p):
    '''
    dec_funcion_param : lista_parametros
                      | empty  
    '''

def p_lista_parametros(p):
    '''
    lista_parametros : ID parDim COLON tipo lista_parametros2
    '''

def p_lista_parametros2(p):
    '''
    lista_parametros2 : COMMA lista_parametros
                      | empty 
    '''

def p_parDim(p):
    '''
    parDim : LBRACK expresion parDim2 RBRACK
           | empty 
    '''

def p_parDim2(p):
    '''
    parDim2 : COMMA expresion
            | empty
    '''

def p_principal(p):
    '''
    principal : PRINCIPAL LPAREN RPAREN bloque
    '''
    global directorioFunciones
    directorioFunciones.func_print('global')

# BLOQUE
def p_bloque(p):
    '''
    bloque : LCURLY estatutos RCURLY
    '''

# ESTATUTOS

def p_estatutos(p):
    '''
    estatutos : estatuto estatutos
              | empty
    '''

def p_estatuto(p):
    '''
    estatuto : asignacion
             | condicion
             | regresa
             | loop_condicional
             | loop_no_condicional
             | llamada_funcion
             | escritura
             | lectura
    '''

# ASIGNACION
def p_asignacion(p):
    '''
    asignacion : variable ASSIGN expresion SEMIC
    '''

def p_ctes(p):
    '''
    ctes : INT_CTE
         | FLOAT_CTE
         | CHAR_CTE
    '''

def p_variable(p):
    '''
    variable : ID varDim
    '''

def p_varDim(p):
    '''
    varDim : LBRACK expresion varDim2 RBRACK
           | empty
    '''

def p_varDim2(p):
    '''
    varDim2 : COMMA expresion
            | empty
    '''

# IF-ELSE
def p_condicion(p):
    '''
    condicion : SI LPAREN expresion RPAREN ENTONCES bloque else 
    '''

def p_else(p):
    '''
    else : SINO bloque
         | empty
    '''

# LOOP CONDICIONAL
def p_loop_condicional(p):
    '''
    loop_condicional : MIENTRAS LPAREN expresion RPAREN HACER bloque
    '''

# LOOP NO CONDICIONAL
def p_loop_no_condicional(p):
    '''
    loop_no_condicional : DESDE variable ASSIGN expresion HASTA expresion HACER bloque
    '''

# LLAMADA FUNCION
def p_llamada_funcion(p) :
    '''
    llamada_funcion : ID LPAREN lista_ids RPAREN SEMIC
    '''

# ESCRITURA
def p_escritura(p) :
    '''
    escritura : ESCRIBE LPAREN escritura2 RPAREN SEMIC
    '''
def p_escritura2(p) :
    '''
    escritura2 : STRING_CTE escritura3
               | expresion escritura3
    '''

def p_escritura3(p) :
    '''
    escritura3 : COMMA escritura2
               | empty
    '''

# LECTURA
def p_lectura(p) : 
    '''
    lectura : LEE LPAREN lista_ids RPAREN SEMIC
    '''

def p_regresa(p):
    '''
    regresa : REGRESA LPAREN variable RPAREN SEMIC
    '''

# EXPRESIONES
def p_expresion(p):
    'expresion : mega_exp expresion1'

def p_expresion1(p):
    '''
    expresion1 : ASSIGN expresion
               | empty
    '''

def p_mega_exp(p):
    'mega_exp : super_exp meg'

def p_meg(p):
    '''
    meg : op_l mega_exp
        | empty
    '''
def p_op_l(p):
    '''
    op_l : AND_LOG
         | OR_LOG
    '''

def p_super_exp(p):
    'super_exp : exp sp'

def p_sp(p):
    '''
    sp : op_r  exp
       | empty
    '''
def p_op_r(p):
    '''
    op_r : LT_LOG
         | GT_LOG
         | LTE_LOG
         | GTE_LOG
         | NE_LOG
         | EQUAL_LOG
    '''

def p_exp(p):
    '''
    exp : termino exp1
    '''

def p_exp1(p):
    '''
    exp1 : op_a exp
         | empty
    '''
def p_op_a(p):
    '''
    op_a : PLUS_OP
         | MINUS_OP
    '''

def p_termino(p):
    '''
    termino : factor term
    '''

def p_term(p):
    '''
    term : op_a1 termino
         | empty
    '''
def p_op_a1(p):
    '''
    op_a1 : MULT_OP
          | DIV_OP
    '''

def p_factor(p):
    '''
    factor : ctes
           | LPAREN exp RPAREN
           | variable
           | llamada_funcion
    '''

def p_empty(p):
    '''empty :'''
    pass
    # print("nulo")

def p_error(p):
    if p:
        print("Error de sintaxis ",p.type, p.value)
        print("Error en la linea "+ str(p.lineno))
        print()
        parser.errok()
    else:
        print("Syntax error at EOF")

############## PUNTOS NEURALGICOS ################
'''
Establecer el tipo actual
'''

def p_pn_SetCurrentType(p):
    '''
    pn_SetCurrentType :
    '''
    global currentType
    currentType = p [-1]
    print(currentType)

'''
Agregar la nueva variable a la tabla de variables
'''

def p_pn_AddVariable(p):
    '''
    pn_AddVariable :
    '''
    global currentFunc
    global varName
    global currentType
    global currentVarName
    global currentCantVars
    global pIDs

    for x in range(currentCantVars): 
        varName = popIDs()
        currentVarName = varName
        directorioFunciones.func_addVar(currentFunc, varName, currentType, 0, 0, 0)
    currentCantVars = 0

'''
Guardar los IDs declarados para cuando se tenga 
el tipo insertarlos a tabla de variables
'''

def p_pn_SaveID(p):
    '''
    pn_SaveID :
    '''
    global pIDs
    global currentCantVars
    currentCantVars += 1
    pushIDs(p[-1])

'''
Agregar nueva funcion al Directorio de Funciones
'''
def p_pn_AddFunc(p):
    '''
    pn_AddFunc :
    '''
    global currentFunc
    global currentType
    global returnBool

    currentCantVars = 0
    currentFunc = p[-1]
    print("CAMBIO DE CONTEXTO CURRENTFUNC = ", currentFunc)
    print('\n')
    directorioFunciones.func_add(currentFunc, currentType,0,0)

    if directorioFunciones.directorio_funciones[currentFunc]['tipo'] == 'void':
        returnBool = False
    else:
        returnBool = True
    print("Return Bool: ", returnBool)
    print('\n')


parser = yacc.yacc()
def main():
    script_dir = os.path.dirname(__file__)
    name = input('File name: ')
    name = "pruebas/" + name + ".txt" 
    path = os.path.join(script_dir,name)
    print(path)
    try:
        f = open(path,'r', encoding='utf-8')
        code = f.read()
        f.close()
        print(code)
        lex_test(code)
        result = parser.parse(code)
    except EOFError:
        print (EOFError)
main()