import ply.yacc as yacc
import os
import codecs
import re
import sys
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

#Impresion de nuevo cuadruplo
def QuadGenerate(operator, leftOperand, rightOperand, result):
    QuadTemporal = (operator, leftOperand, rightOperand, result)
    pushQuad(QuadTemporal)
    NumQuad = nextQuad() - 1
    print(">> Quad {}: ('{}','{}','{}','{}')".format(NumQuad, operator, leftOperand, rightOperand, result))
    
    print("\n")

#Agrega las constantes a la pila de Operandos y Tipos
def pushConstante(constante):
    global d_ints
    global d_floats
    global d_strs
    global d_ch
    
    global cont_IntConstantes
    global cont_FloatConstantes
    global cont_StringConstantes
    global cont_CharConstantes

    if type(constante) == int:
        if constante not in d_ints:
            if cont_IntConstantes < limite_intConstantes:
                d_ints[constante] = cont_IntConstantes
                cont_IntConstantes = cont_IntConstantes + 1
                QuadGenerate('CONS', 'entero', constante, d_ints[constante])
            else:
                print(cont_IntConstantes, limite_intConstantes)
                errorOutOfBounds('Constantes', 'Enteras')
        pushOperando(constante)
        pushMemoria(d_ints[constante])
        pushTipo('entero')
    
    elif type(constante) == float:
        if constante not in d_floats:
            if cont_FloatConstantes < limite_floatConstantes:
                d_floats[constante] = cont_FloatConstantes
                cont_FloatConstantes = cont_FloatConstantes + 1
                QuadGenerate('CONS', 'flotante', constante, d_floats[constante])
            else:
                errorOutOfBounds('Constantes', 'Flotantes')
        pushOperando(constante)
        pushMemoria(d_floats[constante])
        pushTipo('flotante')
    
    elif type(constante) == str:
        if len(constante) > 3: #String
            if constante not in d_strs:
                if cont_StringConstantes < limite_stringsConstantes:
                    d_strs[constante] = cont_StringConstantes
                    cont_StringConstantes += 1
                    print("LENG",len(constante), constante)
                    QuadGenerate('CONS', 'string', constante, d_strs[constante])
                else:
                    errorOutOfBounds('constantes', 'Strings')
            pushOperando(constante)
            pushMemoria(d_strs[constante])
            pushTipo('string')
        else: #Char
            if constante not in d_ch:
                if cont_CharConstantes < limite_charConstantes:
                    d_ch[constante] = cont_CharConstantes
                    cont_CharConstantes += 1
                    QuadGenerate('CONS', 'char', constante, d_ch[constante])
                else:
                    errorOutOfBounds('constantes', 'Chars')
            pushOperando(constante)
            pushMemoria(d_ch[constante])
            pushTipo('char')
    else:
        sys.exit("Error: Tipo de Variable desconocida")


'''
Regresa la direccion de memoria de una constante, y si no está declarada la agrega.
''' 

def getAddConst(constante):

    global d_ints
    global d_floats
    global d_strs
    global d_ch

    global cont_IntConstantes
    global cont_FloatConstantes
    global cont_StringConstantes
    global cont_CharConstantes

    if type(constante) == int:
        if constante not in d_ints:
            if cont_IntConstantes < limite_intConstantes:
                d_ints[constante] = cont_IntConstantes
                cont_IntConstantes += 1
                QuadGenerate('CONS', 'entero', constante, d_ints[constante])
            
            else:
                errorOutOfBounds('constantes', 'Enteras')
        return d_ints[constante]
    
    elif type(constante) == float:
        if constante not in d_floats:
            if cont_FloatConstantes < limite_floatConstantes:
                d_floats[constante] = cont_FloatConstantes
                cont_FloatConstantes += 1
                QuadGenerate('CONS', 'flotante', constante, d_floats[constante])
            
            else:
                errorOutOfBounds('constantes', 'Flotantes')
        return d_floats[constante]
    
    elif type(constante) == str:
        if len(constante) > 1: #String
            if constante not in d_strs:
                if cont_StringConstantes < limite_stringsConstantes:
                    d_strs[constante] = cont_StringConstantes
                    cont_StringConstantes += 1
                    QuadGenerate('CONS', 'string', constante, d_strs[constante])
                else:
                    errorOutOfBounds('constantes', 'Strings')
            
            return d_strs[constante]

        else: #Char
            if constante not in d_ch:
                if cont_CharConstantes < limite_charConstantes:
                    d_ch[constante] = cont_CharConstantes
                    cont_CharConstantes += 1
                    QuadGenerate('CONS', 'char', constante, d_ch[constante])
                else:
                    errorOutOfBounds('constantes', 'Chars')
        
            return d_ch[constante]

    else: 
        sys.exit("Error en getAddConst")


#Impresion de lista de cuadruplos
def QuadGenerateList():
    
    print(directorioFunciones.func_print(GBL))
    print("-------Lista de Cuadruplos: ")

    contador = 0
    # Opción de leer tuplas directamente - TODO: Arreglar
    file = open("obj.txt", "w+")
    for quad in cuadruplos:
        print("{}.\t{},\t{},\t{},\t{}".format(contador,quad[0],quad[1],quad[2],quad[3]))
        contador = contador + 1

        file.write(str(quad) + '\n')
    print("{}.\t{},\t{},\t{},\t{}".format(contador,'FINPROGRAMA','','',''))
    file.write("('FINPROGRAMA', '', '', '')")
    file.close()

#Funcion que muestra menssaje de error cuando los tipos no coinciden
def errorTypeMismatch(leftType,rightType,operador):
    print('Error: Type Mismatch', "leftType: ", leftType,", rightType: ", rightType, ", operador: ", operador)
    sys.exit()
    

#Funcion para mostrar un mensaje de error cuando se llena los maximos posibles valores temporales
def errorOutOfBounds(tipoMemoria,tipoDato):
    sys.exit("Error: Memoria llena; Muchas {} de tipo {}.".format(tipoMemoria,tipoDato))
    

def errorReturnTipo():
    sys.exit("Error: el tipo que intenta retornar no es correcto")

################ Funciones de manejo de memoria##############

'''
Regresa el siguiente temporal disponible, dependiendo el tipo
'''
def nextAvailTemp(tipo):
    global cont_IntTemporales
    global cont_FloatTemporales
    global cont_BoolTemporales
    global avail
    
    if tipo == 'entero':
        if cont_IntTemporales < limite_intTemporales:
            avail = cont_IntTemporales
            cont_IntTemporales += 1
        else:
            errorOutOfBounds('temporales','Enteras')
    elif tipo == 'flotante':
        
        if cont_FloatTemporales < limite_floatTemporales:
            avail = cont_FloatTemporales
            cont_FloatTemporales += 1
        else:
            errorOutOfBounds('temporales','Flotantes')

    elif tipo == 'bool':
        if cont_BoolTemporales < limite_boolTemporales:
            avail = cont_BoolTemporales
            cont_BoolTemporales = cont_BoolTemporales + 1
        else:
           errorOutOfBounds('temporales','Boleanas')
    else:
        avail = -1
        print("Error: Tipo de variable no existente")
        sys.exit()
    return avail

'''
Regresa el siguiente espacio de memoria disponible
'''
def nextAvailMemory(contexto, tipo):
    global cont_IntGlobales
    global cont_IntLocales
    global cont_FloatGlobales
    global cont_FloatLocales
    global cont_StringGlobales
    global cont_StringLocales
    global cont_CharGlobales
    global cont_CharLocales

    posMem = -1
    
    #Global
    if contexto == GBL:

        if tipo == 'entero':
            if cont_IntGlobales < limite_intGlobales:
                posMem = cont_IntGlobales
                cont_IntGlobales += 1
            else:
                errorOutOfBounds(GBL, 'Enteras')
        

        elif tipo == 'flotante':
            if cont_FloatGlobales < limite_floatGlobales:
                posMem = cont_FloatGlobales
                cont_FloatGlobales += 1
            else:
                errorOutOfBounds(GBL, 'Floats')

        elif tipo == 'string':
            if cont_StringGlobales < limite_stringsGlobales:
                posMem = cont_StringGlobales
                cont_StringGlobales += 1
            else:
                errorOutOfBounds(GBL, 'Strings')

        elif tipo == 'char':
            if cont_CharGlobales < limite_charGlobales:
                posMem = cont_CharGlobales
                cont_CharGlobales += 1
            else:
                errorOutOfBounds(GBL, 'Chars')
    #Locales
    else:
        if tipo == 'entero':
            if cont_IntLocales < limite_intLocales:
                posMem = cont_IntLocales
                cont_IntLocales += 1
            else:
                errorOutOfBounds('Locales', 'Enteras')
        

        elif tipo == 'flotante':
            if cont_FloatLocales < limite_floatLocales:
                posMem = cont_FloatLocales
                cont_FloatLocales += 1
            else:
                errorOutOfBounds('Locales', 'Floats')

        elif tipo == 'string':
            if cont_StringLocales < limite_stringsLocales:
                posMem = cont_StringLocales
                cont_StringLocales += 1
            else:
                errorOutOfBounds('Locales', 'Strings')

        elif tipo == 'char':
            if cont_CharLocales < limite_charLocales:
                posMem = cont_CharLocales
                cont_CharLocales += 1
            else:
                errorOutOfBounds('Locales', 'Chars')
    return posMem



'''
Modificador de memoria
'''
def update_pointer(contexto, tipo, cont):
    global cont_IntGlobales
    global cont_IntLocales
    global cont_FloatGlobales
    global cont_FloatLocales
    global cont_StringGlobales
    global cont_StringLocales
    global cont_CharGlobales
    global cont_CharLocales
    

    if contexto == GBL:

        if tipo == 'entero':
            cont_IntGlobales += cont
            if cont_IntGlobales > limite_intGlobales:
                sys.exit('Error: Overflow Enteras Globales')
        
        if tipo == 'flotante':
            cont_FloatGlobales += cont
            if cont_FloatGlobales > limite_floatGlobales:
                sys.exit('Error: Overflow Flotantes Globales')
        
        if tipo == 'string':
            cont_StringGlobales += cont
            if cont_StringGlobales > limite_stringsGlobales:
                sys.exit('Error: Overflow Strings Globales')
        
        if tipo == 'char':
            cont_CharGlobales += cont
            if cont_CharGlobales > limite_charGlobales:
                sys.exit('Error: Overflow Chars Globales')
    else:
        if tipo == 'entero':
            cont_IntLocales += cont
            if cont_IntLocales > limite_intLocales:
                sys.exit('Error: Overflow Enteras Locales')
        
        if tipo == 'flotante':
            cont_FloatLocales += cont
            if cont_FloatLocales > limite_floatLocales:
                sys.exit('Error: Overflow Flotantes Locales')
        
        if tipo == 'string':
            cont_StringLocales += cont
            if cont_StringLocales > limite_stringsLocales:
                sys.exit('Error: Overflow Strings Locales')
        
        if tipo == 'char':
            cont_CharLocales += cont
            if cont_CharLocales > limite_charLocales:
                sys.exit('Error: Overflow Chars Locales')

        
def popMemoria():
    global pMemorias
    pop = pMemorias.pop()
    print("--------------------> POP Memorias")
    print("Pop Memoria = ", pop)
    return pop

def pushMemoria(memoria):
    global pMemorias
    pMemorias.append(memoria)
    print("------>pushMemoria : ", memoria)
    print("pMemoria : ", pMemorias)

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
pDireccionGraficos = [] #Pila de direcciones para los graficos

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

#Variables para Arreglos y matrices
isArray = False
numRenglones = 0
R = 1 #m0
dirBase = 0 #Direccion base
currentConstArrays = []

#Declaracion de espacio de memoria por tipo de memoria
limite_intGlobales = ESPACIO_MEMORIA
limite_floatGlobales = limite_intGlobales + ESPACIO_MEMORIA
limite_stringsGlobales = limite_floatGlobales + ESPACIO_MEMORIA
limite_charGlobales = limite_stringsGlobales + ESPACIO_MEMORIA

limite_intLocales = limite_charGlobales + ESPACIO_MEMORIA
limite_floatLocales = limite_intLocales + ESPACIO_MEMORIA
limite_stringsLocales = limite_floatLocales + ESPACIO_MEMORIA
limite_charLocales = limite_stringsLocales + ESPACIO_MEMORIA

limite_intTemporales = limite_charLocales + ESPACIO_MEMORIA
limite_floatTemporales = limite_intTemporales + ESPACIO_MEMORIA
limite_stringsTemporales = limite_floatTemporales + ESPACIO_MEMORIA
limite_charTemporales = limite_stringsTemporales + ESPACIO_MEMORIA
limite_boolTemporales = limite_charTemporales + ESPACIO_MEMORIA

limite_intConstantes = limite_boolTemporales + ESPACIO_MEMORIA
limite_floatConstantes = limite_intConstantes + ESPACIO_MEMORIA
limite_stringsConstantes = limite_floatConstantes + ESPACIO_MEMORIA
limite_charConstantes = limite_stringsConstantes + ESPACIO_MEMORIA


#Inicio de memoria para Globales
cont_IntGlobales = 0
cont_FloatGlobales = limite_intGlobales
cont_StringGlobales = limite_floatGlobales
cont_CharGlobales = limite_stringsGlobales

#Inicio de memoria para Locales
cont_IntLocales = limite_charGlobales
cont_FloatLocales = limite_intLocales
cont_StringLocales = limite_floatLocales
cont_CharLocales = limite_stringsLocales

#Inicio de memoria para Temporales
cont_IntTemporales = limite_charLocales
cont_FloatTemporales = limite_intTemporales
cont_StringTemporales = limite_floatTemporales
cont_CharTemporales = limite_stringsTemporales
cont_BoolTemporales = limite_charTemporales


#Inicio de memoria para Constatnes
cont_IntConstantes = limite_boolTemporales
cont_FloatConstantes = limite_intConstantes
cont_StringConstantes = limite_floatConstantes
cont_CharConstantes = limite_stringsConstantes

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
    programa : PROGRAMA ID SEMIC dec_variables pn_GOTOprincipal dec_funciones principal
    '''
    print("PROGRAMA \"", p[2], "\" terminado.")
    QuadGenerateList()
    print("pOper : ", pOper)
    print("pOperandos : ", pOperandos)
    print("pTipos: ", pTipos)


#Declaracion de Variables
def p_dec_variables(p):
    '''
    dec_variables : VARIABLES dec_variables2
                  | empty
    '''

def p_dec_variables2(p):
    '''
    dec_variables2 : tipo COLON lista_ids SEMIC dec_variables3
    '''

def p_dec_variables3(p):
    '''
    dec_variables3 : dec_variables2
                   | empty
    '''

def p_lista_ids(p):
    '''
    lista_ids : ID pn_AddVariable DecVarDim lista_ids2
    '''


def p_lista_ids2(p):
    '''
    lista_ids2 : COMMA lista_ids
               | empty
    '''

#Dimensiones
def p_DecVarDim(p):
    '''
    DecVarDim : DecVarDim2 pn_VarDim
              | empty
    '''

def p_DecVarDim2(p):
    '''
    DecVarDim2 : LBRACK pn_VarDim2 INT_CTE pn_VarDim3 RBRACK
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
    dec_funciones2 : FUNCION tipo_func ID pn_AddFunc LPAREN dec_funcion_param RPAREN pn_Funcion2 dec_variables bloque pn_Funcion3
    '''


def p_tipo_func(p):
    '''
    tipo_func : VOID pn_SetCurrentType
              | tipo
    '''

def p_dec_funcion_param(p):
    '''
    dec_funcion_param : lista_parametros
                      | empty  
    '''

def p_lista_parametros(p):
    '''
    lista_parametros : tipo ID pn_Funcion1 lista_parametros2
    '''

def p_lista_parametros2(p):
    '''
    lista_parametros2 : COMMA lista_parametros
                      | empty 
    '''

def p_principal(p):
    '''
    principal : PRINCIPAL pn_Principal1 LPAREN RPAREN bloque
    '''


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
             | funcion_especial_void
    '''

'''
'''
def p_funcion_especial_void(p):
    '''
    funcion_especial_void     : LINEA pn_FuncionEspecial LPAREN pn_Expresion6 exp COMMA direccion RPAREN pn_Expresion7 SEMIC pn_FuncionEspecial2
                              | PUNTO pn_FuncionEspecial LPAREN pn_Expresion6 exp COMMA exp RPAREN pn_Expresion7 SEMIC pn_FuncionEspecial2
                              | CIRCULO pn_FuncionEspecial LPAREN pn_Expresion6 exp RPAREN pn_Expresion7 SEMIC pn_FuncionEspecial2
                              | ARCO pn_FuncionEspecial LPAREN pn_Expresion6 exp COMMA exp RPAREN pn_Expresion7 SEMIC pn_FuncionEspecial2
                              | PENUP pn_FuncionEspecial LPAREN RPAREN SEMIC pn_FuncionEspecial2
                              | PENDOWN pn_FuncionEspecial LPAREN RPAREN SEMIC pn_FuncionEspecial2
                              | GROSOR pn_FuncionEspecial LPAREN pn_Expresion6 exp RPAREN pn_Expresion7 SEMIC pn_FuncionEspecial2
                              | LIMPIAR pn_FuncionEspecial LPAREN RPAREN SEMIC pn_FuncionEspecial2
    '''

def p_direccion(p):
    '''
    direccion : FORWARD pn_SetDireccion
              | BACKWARD pn_SetDireccion
              | RIGHTTURN pn_SetDireccion
              | LEFTTURN pn_SetDireccion
    '''

# ASIGNACION
def p_asignacion(p):
    '''
    asignacion : variable ASSIGN pn_Secuencial1 expresion SEMIC pn_Secuencial2
    '''

def p_ctes(p):
    '''
    ctes : CHAR_CTE pn_CTEChar
         | STRING_CTE pn_CTEString
         | MINUS_OP pn_CTENeg num
         | num
    '''
    if p[1] == '-':
        p[0] = -1 * p[3]
    else:
        p[0] = p[1]
    global negativo
    negativo = False

def p_num(p):
    '''
    num : INT_CTE pn_CTEInt
        | FLOAT_CTE pn_CTEFloat
    '''
    p[0] = p[1]

def p_variable(p):
    '''
    variable : ID pn_Expresion1 varDim
    '''

def p_varDim(p):
    '''
    varDim : LBRACK expresion RBRACK
           | empty
    '''

# IF-ELSE
def p_condicion(p):
    '''
    condicion : SI LPAREN expresion RPAREN pn_Condicion1 ENTONCES bloque else pn_Condicion2
    '''

def p_else(p):
    '''
    else : SINO pn_Condicion3 bloque
         | empty
    '''

# LOOP CONDICIONAL
def p_loop_condicional(p):
    '''
    loop_condicional : MIENTRAS pn_loop_condicional1 LPAREN expresion RPAREN pn_loop_condicional2 HACER bloque pn_loop_condicional3
    '''

# LOOP NO CONDICIONAL
def p_loop_no_condicional(p):
    '''
    loop_no_condicional : DESDE pn_loop_no_condicional1 variable ASSIGN pn_Secuencial1 exp pn_loop_no_condicional2 HASTA pn_loop_no_condicional3 exp pn_loop_no_condicional4 HACER bloque pn_loop_no_condicional5
    '''

def p_varLectura(p):
    '''
    varLectura : ID pn_Expresion1 varLectura2
    '''

def p_varLectura2(p):
    '''
    varLectura2 : COMMA pn_Secuencial4 varLectura
                | empty pn_Secuencial4
    '''

# LECTURA
def p_lectura(p) : 
    '''
    lectura : LEE pn_Secuencial3 LPAREN varLectura RPAREN SEMIC pn_Secuencial5
    '''

# LLAMADA FUNCION
def p_llamada_param(p):
    '''
    llamada_param : expresion pn_FuncionLlamada2 llamada_param2
                  | empty
    '''

def p_llamada_param2(p):
    '''
    llamada_param2 : COMMA llamada_param
                   | empty
    '''

def p_llamada_funcion(p) :
    '''
    llamada_funcion : ID pn_FuncionLlamada1 LPAREN pn_Expresion6 llamada_param RPAREN pn_Expresion7 pn_FuncionLlamada3 SEMIC
                    | ID pn_FuncionLlamada1 LPAREN pn_Expresion6 llamada_param RPAREN pn_Expresion7 pn_FuncionLlamada3
    '''
    p[0] = 'llamada'

def p_regresa(p):
    '''
    regresa : REGRESA pn_Secuencial3 LPAREN exp RPAREN pn_Regresa SEMIC
    '''

# ESCRITURA
def p_escritura(p) :
    '''
    escritura : ESCRIBE pn_Secuencial3 LPAREN escritura2 RPAREN SEMIC pn_Secuencial5
    '''

def p_escritura2(p) :
    '''
    escritura2 : STRING_CTE pn_Secuencial4 escritura3
               | exp pn_Secuencial4 escritura3
    '''

def p_escritura3(p) :
    '''
    escritura3 : COMMA escritura2
               | empty
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
    meg : op_l pn_Expresion10 mega_exp pn_Expresion11
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
    sp : op_r  exp pn_Expresion9
       | empty
    '''
def p_op_r(p):
    '''
    op_r : LT_LOG pn_Expresion8
         | GT_LOG pn_Expresion8
         | LTE_LOG pn_Expresion8
         | GTE_LOG pn_Expresion8
         | NE_LOG pn_Expresion8
         | EQUAL_LOG pn_Expresion8
    '''

def p_exp(p):
    '''
    exp : termino pn_Expresion4 exp1
    '''

def p_exp1(p):
    '''
    exp1 : op_a exp
         | empty
    '''
def p_op_a(p):
    '''
    op_a : PLUS_OP pn_Expresion2
         | MINUS_OP pn_Expresion2
    '''

def p_termino(p):
    '''
    termino : factor pn_Expresion5 term
    '''

def p_term(p):
    '''
    term : op_a1 termino
         | empty
    '''
def p_op_a1(p):
    '''
    op_a1 : MULT_OP pn_Expresion3
          | DIV_OP pn_Expresion3
    '''

def p_factor(p):
    '''
    factor : ctes
           | LPAREN pn_Expresion6 exp RPAREN pn_Expresion7
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
        sys.exit()
        
    else:
        print("Syntax error at EOF")

############## PUNTOS NEURALGICOS ################
'''
Cuadruplo GOTO Main al inicio del programa
'''

def p_pn_GOTOprincipal(p):
    '''
    pn_GOTOprincipal :
    '''
    QuadGenerate('GOTO','','','')
    pushSaltos(nextQuad() - 1)

'''
Generra el cuadruplo de GOTO Main
'''
def p_pn_Principal1(p):
    '''
    pn_Principal1 :
    '''
    global currentFunc
    global cuadruplos

    currentFunc = GBL
    cuadruplos[popSaltos()] = ('GOTO','','',nextQuad())

'''
Cuadruplos de funciones graficas
'''

### FUNCIONES ###
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
    global currentCantVars
    global currentCantParams

    currentCantParams = 0
    currentCantVars = 0
    currentFunc = p[-1]
    print("CAMBIO DE CONTEXTO CURRENTFUNC = ", currentFunc)
    print('\n')
    directorioFunciones.func_add(currentFunc, currentType, currentCantParams, nextQuad())

    if directorioFunciones.directorio_funciones[currentFunc]['tipo'] == 'void':
        returnBool = False
    else:
        returnBool = True
    print("Return Bool: ", returnBool)
    print('\n')

'''
Cuenta la cantidad de parametros que tiene una funcion y agrega los parametros como variables locales de la funcion
'''
def p_pn_Funcion1(p):
    '''
    pn_Funcion1 :
    '''
    global currentFunc
    global currentType
    global currentCantParams
    global currentCantVars
    global varName

    varName = p[-1]
    posMem = nextAvailMemory(currentFunc, currentType)
    directorioFunciones.func_addVar(currentFunc, varName, currentType,0,0,posMem)
    currentCantParams += 1
    currentCantVars += 1

'''
Modifica la acantidad de parametros de una funcion en el directorio de funciones
'''
def p_pn_Funcion2(p):
    '''
    pn_Funcion2 :
    '''

    global currentFunc
    global currentCantParams

    directorioFunciones.func_UpdateParametros(currentFunc,currentCantParams)

'''
Eliminar el directorio de funciones
'''
def p_pn_Funcion3(p):
    '''
    pn_Funcion3 :
    '''

    global returnBool
    global cont_IntLocales
    global cont_FloatLocales
    global cont_StringLocales
    global cont_CharLocales

    global cont_IntTemporales
    global cont_FloatTemporales
    global cont_StringTemporales
    global cont_CharTemporales

    #Reinicio de apuntadores de memoria locales y temporales
    cont_IntLocales = limite_charGlobales
    cont_FloatLocales = limite_intLocales
    cont_StringLocales = limite_floatLocales
    cont_CharLocales = limite_stringsLocales

    #Inicio de memoria para Temporales
    cont_IntTemporales = limite_charLocales
    cont_FloatTemporales = limite_intTemporales
    cont_StringTemporales = limite_floatTemporales
    cont_CharTemporales = limite_stringsTemporales
    cont_BoolTemporales = limite_charTemporales

    QuadGenerate('ENDFUNC','','','')
    returnBool = False
def p_pn_SetDireccion(p):
    '''
    pn_SetDireccion :
    '''
    pDireccionGraficos.append(str(p[-1]))
    print(pDireccionGraficos)


###FUNCIONES ESPECIALES###
'''
guardar la hacia donde se mueve la tortuga o si gira
'''
def p_pn_FuncionEspecial(p):
    '''
    pn_FuncionEspecial :
    '''
    pFunciones.append(str(p[-1]))

'''
crear los cuadruplos de las funciones graficas
'''
def p_pn_FuncionEspecial2(p):
    '''
    pn_FuncionEspecial2 :
    '''
    funName = pFunciones.pop()

    if funName == 'linea':
        direccion = pDireccionGraficos.pop()

        parametroTipo = popTipos()
        parametroNombre = popOperandos()
        parametroMemoria = popMemoria()
        if parametroTipo == 'entero' or parametroTipo == 'float':
            QuadGenerate('linea', parametroMemoria,'',direccion)
        else:
            sys.exit('Error funcion especial linea')
    elif funName == 'punto':
        parametroTipo = popTipos()
        parametroNombre = popOperandos()
        parametroMemoria = popMemoria()

        parametroTipo2 = popTipos()
        parametroNombre2 = popOperandos()
        parametroMemoria2 = popMemoria()
        if ((parametroTipo == 'entero' or parametroTipo == 'float') and (parametroTipo2 == 'entero' or parametroTipo2 == 'float')):
            QuadGenerate('punto', parametroMemoria, parametroMemoria2,'')
        else:
            sys.exit('Error funcion punto')
    elif funName == 'circulo':
        parametroTipo = popTipos()
        parametroNombre = popOperandos()
        parametroMemoria = popMemoria()
        if parametroTipo == 'entero' or parametroTipo == 'float':
            QuadGenerate('circulo', parametroMemoria,'','')
        else:
            sys.exit('Error funcion especial circulo')
    elif funName == 'penup':
        QuadGenerate('penup','','','')
    elif funName == 'pendown':
        QuadGenerate('pendown','','','')
    elif funName == 'limpiar':
        QuadGenerate('limpiar','','','')
    elif funName == 'grosor':
        parametroTipo = popTipos()
        parametroNombre = popOperandos()
        parametroMemoria = popMemoria()
        if parametroTipo == 'entero' or parametroTipo == 'float':
            QuadGenerate('grosor',parametroMemoria,'','')
        else:
            sys.exit('Error funcion especial grosor')
    elif funName == 'arco':
        parametroTipo = popTipos()
        parametroNombre = popOperandos()
        parametroMemoria = popMemoria()

        parametroTipo2 = popTipos()
        parametroNombre2 = popOperandos()
        parametroMemoria2 = popMemoria()
        if ((parametroTipo == 'entero' or parametroTipo == 'float') and (parametroTipo2 == 'entero' or parametroTipo2 == 'float')):
            QuadGenerate('arco', parametroMemoria, parametroMemoria2,'')
        else:
            sys.exit('Error funcion arco')
### LLAMADA FUNCION ####
'''
Verifica que la funcion exista en el directorio de funciones
'''
def p_pn_FuncionLlamada1(p):
    '''
    pn_FuncionLlamada1 :
    '''
    global pFunciones
    global pArgumentos

    funcion = p[-1]

    if funcion in directorioFunciones.directorio_funciones:
        pFunciones.append(funcion)

        QuadGenerate('ERA',funcion,'','')
        pArgumentos.append(0)
    else:
        print("Error: la funcion ",funcion," no existe")
        sys.exit()

'''

'''
def p_pn_FuncionLlamada2(p):
    '''
    pn_FuncionLlamada2 :
    '''
    global pArgumentos
    global pFunciones
    global currentFunc

    argumento = popOperandos()
    TipoArgumento = popTipos()
    ArgumentoMem = popMemoria()
    funcion = pFunciones.pop()
    argumentos = pArgumentos.pop() + 1

    pArgumentos.append(argumentos)
    parametro = 'param' + str(argumentos)
    
    parametrosFuncion = directorioFunciones.directorio_funciones[funcion]['cantParametros']

    lista = directorioFunciones.listaTipos(funcion)

    if parametrosFuncion >= argumentos:
        if lista[argumentos-1] == TipoArgumento:
            QuadGenerate('PARAMETER',ArgumentoMem,'',parametro)
        else:
            print("Error: Parametros incorrectos")
            sys.exit()
    else:
        print("Error: numero de argumentos incorrecto")
        sys.exit()

    pFunciones.append(funcion)

'''
'''
def p_pn_FuncionLlamada3(p):
    '''
    pn_FuncionLlamada3 :
    '''

    global returnBool
    global pFunciones
    global pArgumentos

    argumentos = pArgumentos.pop()
    funcion = pFunciones.pop()

    
    if argumentos == directorioFunciones.directorio_funciones[funcion]['cantParametros']:
        quadLlamada = directorioFunciones.directorio_funciones[funcion]['cantQuads']

        #Generar GOSUB, nombre funcion, '', memoria inicial
        QuadGenerate('GOSUB',funcion, nextQuad() + 1, quadLlamada)

    else:
        print("Error: Mismatch de Argumentos")
        sys.exit()
    
    tipo = directorioFunciones.directorio_funciones[funcion]['tipo']
    if tipo != 'void':
        temporal = nextAvailTemp(tipo)
        QuadGenerate('=', funcion, '', temporal)
        pushOperando(temporal)
        pushMemoria(temporal)
        pushTipo(tipo)

### CONSTANTES ###
'''
Indicar constante negativa
'''
def p_pn_CTENeg(p):
    '''
    pn_CTENeg :
    '''
    global negativo
    negativo = True

def p_pn_CTEInt(p):
    '''
    pn_CTEInt :
    '''
    if negativo:
        pushConstante(-1 * p[-1])
    else:
        pushConstante(p[-1])

def p_pn_CTEFloat(p):
    '''
    pn_CTEFloat :
    '''
    if negativo:
        pushConstante(-1 * p[-1])
    else:
        pushConstante(p[-1])

def p_pn_CTEChar(p):
    '''
    pn_CTEChar :
    '''
    pushConstante(p[-1])

def p_pn_CTEString(p):
    '''
    pn_CTEString :
    '''
    pushConstante(p[-1])

### EXPRESIONES ###
'''
Anadir ID y Tipo a pOper y pTipo 
'''
def p_pn_Expresion1(p):
    '''
    pn_Expresion1 :
    '''
    global currentFunc
    global directorioFunciones
    global pOperandos
    global pTipos
    global currentVarName
    global forBool
    global varFor

    id = p[-1]
    tipo = directorioFunciones.func_searchVarType(currentFunc, id)
    if not tipo:
        print("Variable no en contexto actual, cambiando a global")
        tipo = directorioFunciones.func_searchVarType(GBL, id)
    if not tipo:
        print("Error: Variable ", id, " no declarada")
        sys.exit()
    
    varPosMem = directorioFunciones.func_memoria(currentFunc, id)
    if not varPosMem:
        varPosMem = directorioFunciones.func_memoria(GBL, id)
    
    if varPosMem < 0:
        print("Error: Variable ", id, " no declarada")
        sys.exit()
    
    if forBool:
        varFor = id
    
    dimBool = directorioFunciones.func_isVarDimensionada(currentFunc,id)
    print("Expresion1, Dimensionada", dimBool)

    if dimBool == -1:
        print("Variable no en contexto actual, cambiando a global")
        dimBool = directorioFunciones.func_isVarDimensionada(GBL, id)
    
    if dimBool == 1:
        isArray = True
        currentVarName = id
    elif dimBool == 0:
        isArray = False
    else:
        isArray = False
        sys.exit("Error. No se ha declarado la variable: ", id)
        return
    pushOperando(id)
    pushMemoria(varPosMem)
    pushTipo(tipo)
    print("\n")

'''
Anadir + o - al pOper
'''
def p_pn_Expresion2(p):
    '''
    pn_Expresion2 :
    '''
    global pOper
    if p[-1] not in OP_SUMARESTA:
        print("Error: Operador no esperado")
        sys.exit()
    else:
        pushOperador(p[-1])

'''
Anadir * o / al pOper
'''
def p_pn_Expresion3(p):
    '''
    pn_Expresion3 :
    '''

    global pOper
    if p[-1] not in OP_MULTDIV:
        print("Error: Operador no esperado")
        sys.exit()
    else:
        pushOperador(p[-1])

'''
Revisar si el top de pOper es un + o - para generar el cuadruplo
'''
def p_pn_Expresion4(p):
    '''
    pn_Expresion4 :
    '''
    if topOperador() in OP_SUMARESTA:
        rightOperand = popOperandos()
        rightType = popTipos()
        rightMem = popMemoria()
        leftOperand = popOperandos()
        leftMem = popMemoria()
        leftType = popTipos()
        operador = popOperadores()

        global cuboSem
        resultType = cuboSem.getType(leftType,rightType,operador)

        if resultType == "error":
            errorTypeMismatch(leftType,rightType,operador)
        else:
            temporal = nextAvailTemp(resultType)
            QuadGenerate(operador, leftMem, rightMem, temporal)
            pushOperando(temporal)
            pushMemoria(temporal)
            pushTipo(resultType)

'''
Revisar si el top de pOper es un * o / para generar el cuadruplo
'''
def p_pn_Expresion5(p):
    '''
    pn_Expresion5 :
    '''
    if topOperador() in OP_MULTDIV:
        rightOperand = popOperandos()
        rightType = popTipos()
        rightMem = popMemoria()
        leftOperand = popOperandos()
        leftMem = popMemoria()
        leftType = popTipos()
        operador = popOperadores()

        global cuboSem
        resultType = cuboSem.getType(leftType,rightType,operador)

        if resultType == "error":
            errorTypeMismatch(leftType,rightType,operador)
        else:
            temporal = nextAvailTemp(resultType)
            QuadGenerate(operador, leftMem, rightMem, temporal)
            pushOperando(temporal)
            pushMemoria(temporal)
            pushTipo(resultType)

'''
Agregar fondo falso
'''
def p_pn_Expresion6(p):
    '''
    pn_Expresion6 :
    '''
    global pOper
    pushOperador('(')
    print("Fondo Falso Agregado")

'''
Quitar fondo falso
'''
def p_pn_Expresion7(p):
    '''
    pn_Expresion7 :
    '''
    popOperadores()
    print("Fondo Falso Quitado")

'''
Meter operador relacional a pOper
'''
def p_pn_Expresion8(p):
    '''
    pn_Expresion8 :
    '''
    if p[-1] not in OP_REL:
        print("Error: Operador no esperado")
        sys.exit()
    else:
        pushOperador(p[-1])

'''
Verificar si el top de la pila de operadores es un operador relacional y generar cuadruplo
'''
def p_pn_Expresion9(p):
    '''
    pn_Expresion9 : 
    '''
    if topOperador() in OP_REL:
        rightOperand = popOperandos()
        rightType = popTipos()
        rightMem = popMemoria()
        leftOperand = popOperandos()
        leftMem = popMemoria()
        leftType = popTipos()
        operador = popOperadores()

        global cuboSem
        resultType = cuboSem.getType(leftType,rightType,operador)

        if resultType == "error":
            errorTypeMismatch(leftType,rightType,operador)
        else:
            temporal = nextAvailTemp(resultType)
            QuadGenerate(operador, leftMem, rightMem, temporal)
            pushOperando(temporal)
            pushMemoria(temporal)
            pushTipo(resultType)
'''
Meter un operador logico a pOper
'''

def p_pn_Expresion10(p):
    '''
    pn_Expresion10 :
    '''
    global pOper
    if p[-1] not in OP_LOGICOS:
        print("Error: Operador no esperado")
        sys.exit()
    else:
        pushOperador(p[-1])

'''
Verificar que el top de la pila de operadores es un operador logico
'''
def p_pn_pn_Expresion11(p):
    '''
    pn_Expresion11 :
    '''
    if topOperador() in OP_LOGICOS:
        rightOperand = popOperandos()
        rightType = popTipos()
        rightMem = popMemoria()
        leftOperand = popOperandos()
        leftMem = popMemoria()
        leftType = popTipos()
        operador = popOperadores()

        global cuboSem
        resultType = cuboSem.getType(leftType,rightType,operador)

        if resultType == "error":
            errorTypeMismatch(leftType,rightType,operador)
        else:
            temporal = nextAvailTemp(resultType)
            QuadGenerate(operador, leftMem, rightMem, temporal)
            pushOperando(temporal)
            pushMemoria(temporal)
            pushTipo(resultType)



### SECUENCIAL ###
'''
Mete '=' a la pila de operadores
'''
def p_pn_Secuencial1(p):
    '''
    pn_Secuencial1 :
    '''
    global pOper
    if p[-1] not in OP_ASIG:
        print('Error: Operador no esperado')
        sys.exit()
    else:
        pushOperador(p[-1])

'''
Revisar el top de la pila de los operadores si hay una asignacion
'''
def p_pn_Secuencial2(p):
    '''
    pn_Secuencial2 :
    '''
    if topOperador() in OP_ASIG:
        rightOp = popOperandos()
        rightType = popTipos()
        rightMem = popMemoria()
        leftOp = popOperandos()
        leftMem = popMemoria()
        leftType = popTipos()
        operador = popOperadores()

        global cuboSem
        global directorioFunciones

        resultType = cuboSem.getType(leftType, rightType, operador)

        if directorioFunciones.var_exist(currentFunc, leftOp) or directorioFunciones.var_exist(GBL, leftOp):
            if resultType == 'error':
                print("Error: Operacion invalida")
                sys.exit()
            else:
                QuadGenerate(operador, rightMem,'',leftMem)
        else:
            print("Error al intentar asignar una variable")


'''
Meter lectura, escritura o regresar a la pila
'''
def p_pn_Secuencial3(p):
    '''
    pn_Secuencial3 :
    '''
    global pOper
    if p[-1] not in OP_SECUENCIALES:
        print("Error: operador secuencial no esperado ", p[-1])
        sys.exit()
    else:
        pushOperador(p[-1])

'''
Checar si el top de la pila de operadores es lectura, escritura o regreso
'''
def p_pn_Secuencial4(p):
    '''
    pn_Secuencial4 :
    '''

    global cuboSem
    if topOperador() in OP_SECUENCIALES:
        print("Ejecutando pn_Secuencial2")
        operando = popOperandos()
        rightType = popTipos()
        rightMem = popMemoria()
        operador = popOperadores()

        resultType = cuboSem.getType(operador, rightType, '')

        if resultType == "error":
            errorTypeMismatch('',rightType,operador)
        else:
            QuadGenerate(operador, rightMem, '', operador)
            pushOperador(operador)

'''
Hacer pop a la pila de operadores
'''
def p_pn_Secuencial5(p):
    '''
    pn_Secuencial5 :
    '''
    popOperadores()

### RETURN ###

def p_pn_Regresa(p):
    '''
    pn_Regresa :
    '''
    global currentFunc
    global returnBool
    if returnBool:
        print(pOperandos)
        print(pTipos)
        operador = popOperadores()
        operandoRetorno = popOperandos()
        tipoRetorno = popTipos()
        memRetorno = popMemoria()

        if directorioFunciones.directorio_funciones[currentFunc]['tipo'] == tipoRetorno:
            QuadGenerate(operador, '','',memRetorno)
        else:
            errorReturnTipo()
    else:
        print("Error: esta funcion no debe regresar nada")
        sys.exit()

### CONDICION ###

'''
Genera el cuadruplo GOTOF en la condicion SI despues de recibir el booleano generado por la expresion
'''
def p_pn_Condicion1(p):
    '''
    pn_Condicion1 :
    '''
    global cuadruplos
    memPos = popMemoria()
    tipo = popTipos()
    if(tipo != "error"):
        result = popOperandos()
        QuadGenerate('GOTOF', result,'','')
        pushSaltos(nextQuad()-1)
    else:
        sys.exit('Error al generar GOTOF')

'''
Rellena el cuadruplo para saber cuando terminar la condicion
'''
def p_pn_Condicion2(p):
    '''
    pn_Condicion2 :
    '''
    global cuadruplos

    final = popSaltos()

    QuadTemporal = (cuadruplos[final][0], cuadruplos[final][1], cuadruplos[final][2], nextQuad())
    cuadruplos[final] = QuadTemporal

'''
Genera el cuadruplo GOTO para SINO y completa el cuadruplo
'''
def p_pn_Condicion3(p):
    '''
    pn_Condicion3 :
    '''
    global cuadruplos
    QuadGenerate('GOTO', '', '', '')
    falso = popSaltos()
    pushSaltos(nextQuad() - 1)
    QuadTemporal = (cuadruplos[falso][0], cuadruplos[falso][1], cuadruplos[falso][2], nextQuad())
    cuadruplos[falso] = QuadTemporal

### LOOPS ###
'''
Insertar el siguiente cuadruplo a pSaltos para guardar la ubicacion donde regresara al final del ciclo para volver a evaluar
'''
def p_pn_loop_condicional1(p):
    '''
    pn_loop_condicional1 :
    '''
    pushSaltos(nextQuad())

'''
Generar el cuadruplo GOTOF
'''
def p_pn_loop_condicional2(p):
    '''
    pn_loop_condicional2 :
    '''
    tipo = popTipos()
    memPos = popMemoria()
    if tipo != "error":
        result = popOperandos()
        QuadGenerate('GOTOF', result, '', '')
        pushSaltos(nextQuad() - 1)
    else:
        errorTypeMismatch(tipo,'','GOTOF')

'''
Generar el cuadruplo GOTO para regresar al inicio del ciclo y evaluar la condicion y rellenar el GOTOF
'''
def p_pn_loop_condicional3(p):
    '''
    pn_loop_condicional3 :
    '''

    end = popSaltos()
    retorno = popSaltos()
    QuadGenerate('GOTO','','',retorno)


    #Rellenar
    quadTemporal = (cuadruplos[end][0], cuadruplos[end][1],cuadruplos[end][2],nextQuad())
    cuadruplos[end] = quadTemporal

'''
Activar bandera de ciclo no condicional DESDE
'''
def p_pn_loop_no_condicional1(p):
    '''
    pn_loop_no_condicional1 :
    '''
    global forBool
    forBool = True

'''
Verificacion si existen las variables y los tipos son compatibles
'''
def p_pn_loop_no_condicional2(p):
    '''
    pn_loop_no_condicional2 :
    '''

    if topOperador() in OP_ASIG:
        rightOperand = popOperandos()
        rightType = popTipos()
        leftOperand = popOperandos()
        leftType = popTipos()
        operador = popOperadores()

        global cuboSem
        global directorioFunciones

        resultado = cuboSem.getType(leftType,rightType,operador)

        if directorioFunciones.var_exist(currentFunc, leftOperand) or directorioFunciones.var_exist(GBL, leftOperand):
            if resultado == 'error':
                print("Error: operacion invalida")
                sys.exit()
            else:
                QuadGenerate(operador, rightOperand, '', leftOperand)
        else:
            print('Error')
            sys.exit()

'''
'''
def p_pn_loop_no_condicional3(p):
    '''
    pn_loop_no_condicional3 :
    '''
    pushOperando(varFor)

    tipo = directorioFunciones.func_searchVarType(currentFunc, varFor)

    if not tipo:
        tipo = directorioFunciones.func_searchVarType(GBL, varFor)
    
    if not tipo:
        print("Error: variable no declarada")
        sys.exit()
    
    pushTipo(tipo)
    pushOperador('<=')
    pushSaltos(nextQuad())

'''
'''
def p_pn_loop_no_condicional4(p):
    '''
    pn_loop_no_condicional4 :
    '''
    if topOperador() in OP_REL:
        rightOperand = popOperandos()
        rightType = popTipos()
        leftOperand = popOperandos()
        leftType = popTipos()
        operador = popOperadores()

        global cuboSem
        tipo = cuboSem.getType(leftType, rightType, operador)

        if tipo == 'error':
            errorTypeMismatch(leftType,rightType,operador)
        else:
            temporal = nextAvailTemp(tipo)
            QuadGenerate(operador, leftOperand, rightOperand, temporal)
            pushOperando(temporal)
            pushTipo(tipo)
        
        tipo_exp = popTipos()
        if (tipo_exp != 'bool' or tipo_exp == 'error'):
            errorTypeMismatch(leftType,rightType,operador)
        else:
            result = popOperandos()
            QuadGenerate('GOTOF', result, '', '')
            pushSaltos(nextQuad()-1)

'''
'''
def p_pn_loop_no_condicional5(p):
    '''
    pn_loop_no_condicional5 :
    '''
    end = popSaltos()
    retorno = popSaltos()
    QuadGenerate('GOTO','','', retorno)

    temporal = (cuadruplos[end][0], cuadruplos[end][1], cuadruplos[end][2], nextQuad())
    cuadruplos[end] = temporal #FILL (end, cont) 



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
    varName = p[-1]
    currentVarName = varName
    posMem = nextAvailMemory(currentFunc,currentType)
    print("Posicion memoria",posMem)
    directorioFunciones.func_addVar(currentFunc, varName, currentType, 0, 0, posMem)
    currentCantVars += 1

### ARREGLOS Y MATRICES ###

'''
Guardar la cantidad de renglones que tiene la variable
'''
def p_pn_Renglones(p):
    '''
    pn_Renglones :
    '''
    global numRenglones
    numRenglones = p[-2]


'''
Actualizar bandera de id como arreglo
'''
def p_pn_VarDim2(p):
    '''
    pn_VarDim2 :
    '''
    global isArray
    isArray = True

'''
Guardar limite de columnas
'''
def p_pn_VarDim3(p):
    '''
    pn_VarDim3 :
    '''
    global R
    global numColumnas
    global directorioFunciones
    global currentFunc
    global currentVarName

    columnas = p[-1]
    if columnas > 0:
        R = R * columnas # R = (LimSup - LimInf + 1) * R
        numColumnas = columnas
        directorioFunciones.func_updateDim(currentFunc,currentVarName,0,columnas)
    else:
        sys.exit("Error : Index de arreglo invalido: ", columnas)


'''
Actualizar el pointer de memoria tomando los espacios necesarios para el arreglo
'''
def p_pn_VarDim(p):
    '''
    pn_VarDim :
    '''
    global R
    global directorioFunciones
    global currentFunc
    global currentVarName
    global isArray
    global currentConstArrays
    numEspacios = R - 1

    currentType = directorioFunciones.func_searchVarType(currentFunc, currentVarName)
    
    update_pointer(currentFunc, currentType, numEspacios)

    #Reseteo
    R = 1
    isArray = False
    currentConstArrays = []

def p_pn_DimAccess(p):
    '''
    pn_DimAccess :
    '''

    global isArray
    global pDim
    isArray = True

    id = popOperandos()
    memoria = popMemoria()
    tipo = popTipos()

    pDim.append(id)

'''
Acceder al indice del arreglo
'''

def p_pn_AccederArreglo(p):
    '''
    pn_AccederArreglo :
    '''

    global isArray
    global currentFunc
    global currentVarName

    #Valor que va acceder al arreglo
    id = popOperandos()
    memoria = popMemoria()
    tipo = popTipos()
    #variable dimensionada
    dim = pDim.pop()

    if isArray:
        #Tiene que ser entero
        if tipo != 'entero':
            sys.exit('Error: Tiene que ser valor entero para acceder al arreglo')

        varDimensiones = directorioFunciones.func_getDims(currentFunc,dim)

        if varDimensiones == -1:
            varDimensiones = directorioFunciones.func_getDims(GBL, dim)

            if varDimensiones == -1:
                sys.exit("Error: Variable Dimensionada no existe")
        
        #Cuadruplo verifica
        QuadGenerate('VER', memoria, 0, varDimensiones[0]-1)

        #Si no es Matriz
        if varDimensiones[1] == 0:
            #Memoria Base
            posicionMemoria = directorioFunciones.func_memoria(currentFunc, dim)
            if not posicionMemoria:
                posicionMemoria = directorioFunciones.func_memoria(GBL,dim)
            if posicionMemoria < 0:
                sys.exit("Error variable no declarada ", dim)
            
            tipoActual = directorioFunciones.func_searchVarType(currentFunc,dim)
            if not tipoActual:
                tipoActual = directorioFunciones.func_searchVarType(currentFunc, dim)
                sys.exit('Error variable no declarada ', dim)
            
            tMemoria = nextAvailTemp('entero')
            QuadGenerate('+', '{' + str(posicionMemoria) + '}', memoria, tMemoria)
            valorTMem = str(tMemoria) + '!'

            pushOperando(dim)
            pushMemoria(valorTMem)
            pushTipo(tipoActual)
            isArray = False
            currentVarName = ''
    else:
        sys.exit("Error no se puede acceder variable no dimensionada")



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