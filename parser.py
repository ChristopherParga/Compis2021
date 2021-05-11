import ply.yacc as yacc
import os
import codecs
import re
from lexer import tokens, lex_test
from sys import stdin
from DirFunc import *
from CuboSemantico import *
from sys import stdin

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
def errorTypeMismatch():
    sys.exit('Error: Type Mismatch')
    

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
    
    if tipo == 'int':
        if cont_IntTemporales < limite_intTemporales:
            avail = cont_IntTemporales
            cont_IntTemporales += 1
        else:
            errorOutOfBounds('temporales','Enteras')
    elif tipo == 'float':
        
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

        if tipo == 'int':
            if cont_IntGlobales < limite_intGlobales:
                posMem = cont_IntGlobales
                cont_IntGlobales += 1
            else:
                errorOutOfBounds(GBL, 'Enteras')
        

        elif tipo == 'float':
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
        if tipo == 'int':
            if cont_IntLocales < limite_intLocales:
                posMem = cont_IntLocales
                cont_IntLocales += 1
            else:
                errorOutOfBounds('Locales', 'Enteras')
        

        elif tipo == 'float':
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

        if tipo == 'int':
            cont_IntGlobales += cont
            if cont_IntGlobales > limite_intGlobales:
                sys.exit('Error: Overflow Enteras Globales')
        
        if tipo == 'float':
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
        if tipo == 'int':
            cont_IntLocales += cont
            if cont_IntLocales > limite_intLocales:
                sys.exit('Error: Overflow Enteras Locales')
        
        if tipo == 'float':
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
isMatrix = False
numRenglones = 0
numColumnas = 0
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
    DecVarDim2 : LBRACK pn_VarDim2 INT_CTE pn_VarDim3 DecVarDim3 RBRACK
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

def p_llamada_param(p):
    '''
    llamada_param : expresion llamada_param2
    '''

def p_llamada_param2(p):
    '''
    llamada_param2 : COMMA expresion
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

# LECTURA
def p_lectura(p) : 
    '''
    lectura : LEE LPAREN llamada_param RPAREN SEMIC
    '''
    print('lectura')

# LLAMADA FUNCION
def p_llamada_funcion(p) :
    '''
    llamada_funcion : ID LPAREN llamada_param RPAREN SEMIC
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
Cuadruplo GOTO Main al inicio del programa
'''

def p_pn_GOTOprincipal(p):
    '''
    pn_GOTOprincipal :
    '''
    QuadGenerate('GOTO','','','')
    pushSaltos(nextQuad() - 1)

'''
Genera el cuadruplo de GOTO Main
'''

def p_pn_GOTOprincipal2(p):
    '''
    pn_GOTOprincipal2 :
    '''
    global currentFunc
    global cuadruplos

    currentFunc = GBL
    cuadruplos[popSaltos()] = ('GOTO', '', '', nextQuad())

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
    directorioFunciones.func_addVar(currentFunc, varName, currentType, 0, 0, posMem)
    currentCantVars += 1

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
        R = R * columnas 
        numColumnas = columnas
        directorioFunciones.func_updateDim(currentFunc,currentVarName,0,columnas)
    else:
        sys.exit("Error : Index de arreglo invalido: ", columnas)

'''
Guardar renglones (matriz)
'''
def p_pn_VarDim4(p):
    '''
    pn_VarDim4 :
    '''
    global R
    global numRenglones
    global directorioFunciones
    global currentFunc
    global currentVarName
    global isMatrix

    isMatrix = True
    renglones = p[-1]
    if renglones > 0:
        R = R * renglones 
        print("pn_VarDim4.  R = ", R)
        numRenglones = renglones

        directorioFunciones.func_updateDim(currentFunc, currentVarName, renglones, -1)
    else: 
        sys.exit("Error. Index menor o igual a cero no es valido")   

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

    currentType = directorioFunciones.func_searchVarType(currentType, currentVarName)
    
    update_pointer(currentFunc, currentType, numEspacios)

    R = 1
    isArray = False
    currentConstArrays = []




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