from memoriaVirtual import *
from easygraphics import *
from easygraphics.turtle import *

'''
Declaracion de constantes
'''
GBL = 'globales'
LCL = 'locales'
CONST_TEMPORAL = 'temporal'
CONST_EJECUCION = 'ejecucion'
CONST_RETORNO_VALOR = 'retorno'
CONST_FUNCION_RETORNO = 'funcion'
ESPACIO_MEMORIA = 1000

'''
Inicializamos las instancias de memoria de defaul
Globla y funcion principal
'''
mem_GLOBAL = memoriaVirtual('global')
mem_PRINCIPAL = memoriaVirtual('principal')

constLista = []
cuaLista = []
cuaIndice = 0
cuadruplo = ()
pilaRetorno = []
pilaFuncion = []
sigCuaIndice = -1

pilaTemporal = []
pilaEjecucion = []
pilaCorriendo = ''

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

'''
Funciones de control de las pilas
'''
# Funcion para hacer push a las diferenes pilas y poder manear las diferentes instancias de memmoria
def push(pilaNom, mem):
    if pilaNom == CONST_TEMPORAL:
        global pilaTemporal
        pilaTemporal.append(mem)
    elif pilaNom == CONST_EJECUCION:
        global pilaEjecucion
        pilaEjecucion.append(mem)
    elif pilaNom == CONST_RETORNO_VALOR:
        global pilaRetorno
        pilaRetorno.append(mem)
    elif pilaNom == CONST_FUNCION_RETORNO:
        global pilaFuncion
        pilaFuncion.append(mem)
# Funcion para hacer pop a las diferenes pilas y poder manear las diferentes instancias de memmoria
def pop(pilaNom):
    if pilaNom == CONST_TEMPORAL:
        global pilaTemporal
        return pilaTemporal.pop()
    elif pilaNom == CONST_EJECUCION:
        global pilaEjecucion
        return pilaEjecucion.pop()
    elif pilaNom == CONST_RETORNO_VALOR:
        global pilaRetorno
        return pilaRetorno.pop()
    elif pilaNom == CONST_FUNCION_RETORNO:
        global pilaFuncion
        return pilaFuncion.pop()
# Funcion para sacar pop de las principales pilas a las diferenes pilas y poder manear las diferentes instancias de memmoria
def top(pilaNom):
    if pilaNom == CONST_TEMPORAL:
        global pilaTemporal
        aux = len(pilaTemporal) - 1
        if (aux < 0):
            return 'vacia'
        return pilaTemporal[aux]
    elif pilaNom == CONST_EJECUCION:
        global pilaEjecucion
        aux = len(pilaEjecucion) - 1
        if (aux < 0):
            return 'vacia'
        return pilaEjecucion[aux]

# Declaramos la primera instancia de la memoria principal
push(CONST_EJECUCION, mem_PRINCIPAL)

'''
Funcion que permite sacar los valores de la clase memoria, mandando la instacnia de memoria, la direccion y el tipo
'''
def getValor(memoriaVirtual, memDireccion, memTipo):
    global mem_GLOBAL
    try: # En caso de que sea un apuntador
        if memDireccion[-1] == '!':
            memDireccion = getValor(memoriaVirtual, memDireccion[0:-1], getTipo(memDireccion[0:-1]))
            memTipo = getTipo(memDireccion)
    except:
        pass
    seccion = getSeccion(memDireccion)

    try:
        if seccion == GBL:
            valor = mem_GLOBAL.obtenerValorDeDireccion(memDireccion, memTipo)
        elif seccion == LCL:
            valor = memoriaVirtual.obtenerValorDeDireccion(memDireccion, memTipo)
        else:
            print("Error Maquina Virtual: No se encontró sección {} de memoria".format(seccion))
            sys.exit()
    except:
        print("Error Maquina Virtual: ", sys.exc_info()[0], " en seccion {}, en direccion {}, en indice {}.".format(seccion, memDireccion, cuaIndice))
        sys.exit()
    return valor
'''
Funcion que permite meter los valores a la clase memoria, mandando la instacnia de memoria, la direccion y el tipo
'''
def llenarValor(memoriaVirtual, memDireccion, memTipo, valor):
    global mem_GLOBAL
    try: # En caso de que sea un apuntador
        if memDireccion[-1] == '!':
            memDireccion = getValor(memoriaVirtual, memDireccion[0:-1], getTipo(memDireccion[0:-1]))
            memTipo = getTipo(memDireccion)
    except:
        pass
    seccion = getSeccion(memDireccion)

    if seccion == GBL:
        mem_GLOBAL.guardarValor(memDireccion, memTipo, valor)
    elif seccion == LCL:
        memoriaVirtual.guardarValor(memDireccion, memTipo, valor)
    else:
        print("Error Maquina Virtual: No se encontró sección de memoria")
        sys.exit()
        return

'''
Esta funcion ayuda a sacar la seccion de la memoria, mediante el numero
'''
def getSeccion(direccion):
    global pilaCorriendo
    try:
        if direccion[-1] == '!':
            direccion = getValor(pilaCorriendo, direccion[0:-1], getTipo(direccion[0:-1]))
    except:
        pass
    direccion = int(direccion)
    # GLOBALES y CONSTANTES se guardan donde mismo
    if ((direccion >= 0 and direccion < limite_charGlobales) or (direccion >= limite_boolTemporales and direccion <= limite_charConstantes)):
        return GBL
    # LOCALES y TEMPORALES se guardan donde mismo
    if ((direccion >= limite_charGlobales and direccion < limite_charLocales) or (direccion >= limite_charLocales and direccion < limite_boolTemporales)):
        return LCL
    else:
        print("Error Maquina Virtual: {} no se encuentra dentro de ninguna seccion".format(direccion))
        sys.exit()
        return

'''
Esta funcion permite sacar el tipo, al que pertenece la direccion que se le envia
'''
def getTipo(direccion):
    global pilaCorriendo
    try: 
        if direccion[-1] == '!':
            direccion = getValor(pilaCorriendo, direccion[0:-1], getTipo(direccion[0:-1]))
    except:
        pass
    direccion = int(direccion)
    if ((direccion >= 0 and direccion < limite_intGlobales) or (direccion >= limite_charGlobales and direccion < limite_intLocales) or (direccion >= limite_charLocales and direccion < limite_intTemporales) or (direccion >= limite_boolTemporales and direccion < limite_intConstantes)):
        return 'entero'
    if ((direccion >= limite_intGlobales and direccion < limite_floatGlobales) or (direccion >= limite_intLocales and direccion < limite_floatLocales) or (direccion >= limite_intTemporales and direccion < limite_floatTemporales) or (direccion >= limite_intConstantes and direccion < limite_floatConstantes)):
        return 'flotante'
    if ((direccion >= limite_floatGlobales and direccion < limite_stringsGlobales) or (direccion >= limite_floatLocales and  direccion < limite_stringsLocales) or (direccion >= limite_floatTemporales and direccion < limite_stringsTemporales) or (direccion >= limite_floatConstantes and direccion < limite_stringsConstantes)):
        return 'string'
    if ((direccion >= limite_stringsGlobales and direccion < limite_charGlobales) or (direccion >= limite_stringsLocales and direccion <limite_charLocales) or (direccion >= limite_stringsTemporales and direccion < limite_charTemporales) or (direccion >= limite_stringsConstantes and direccion < limite_charConstantes)):
        return 'char'
    if (direccion >= limite_charTemporales and direccion < limite_boolTemporales):
        return 'bool'
    else:
        print("Error Maquina Virtual: {} no se encuentra dentro del rango de ningun tipo de variable".format(direccion))
        sys.exit()
        return
'''
Funcion operadores, para sacar el signo
'''
def operadores(signo):
    global cuadruplo
    global pilaCorriendo
    tipo1 = getTipo(cuadruplo[1])
    tipo2 = getTipo(cuadruplo[2])
    valor1 = getValor(pilaCorriendo, cuadruplo[1], tipo1)
    valor2 = getValor(pilaCorriendo, cuadruplo[2], tipo2)

    if tipo1 == 'entero':
        valor1 = int(valor1)
    elif tipo1 == 'flotante':
        valor1 = float(valor1)

    if tipo2 == 'entero':
        valor2 = int (valor2)
    elif tipo2 == 'flotante':
        valor2 = float(valor2)

    if signo == '+':
        res = valor1 + valor2
    elif signo == '-':
        res = valor1 - valor2
    elif signo == '*':
        res = valor1 * valor2
    elif signo == '/':
        res = valor1 / valor2
    elif signo == '==':
        res = valor1 == valor2
    elif signo == '<':
        res = valor1 < valor2
    elif signo == '>':
        res = valor1 > valor2
    elif signo == '<=':
        res = valor1 <= valor2
    elif signo == '>=':
        res = valor1 >= valor2
        #print(getTipo(cuadruplo[3]))
    elif signo == '!=':
        res = valor1 != valor2
    elif signo == '|':
        res = True if valor1 == valor2 and valor1 == False and valor2 == False else False
    elif signo == '&':
        res = True if valor1 == valor2 and valor1 == True else False
        print(getTipo(cuadruplo[3]))

    llenarValor(pilaCorriendo, cuadruplo[3], getTipo(cuadruplo[3]), res)


def main():
        # Se declaran las variables globales a utilizar
    global constLista
    global cuaLista
    global cuaIndice
    global cuadruplo
    global mem_GLOBAL
    global pilaRetorno
    global sigCuaIndice
    global pilaCorriendo
    create_world(400,400)
    set_speed(1)

    # Ciclo que permite guardar todos los constantes antes de correr los demas cuadruplo
    for cons in constLista:
        llenarValor(mem_GLOBAL, cons[3], cons[1], cons[2])
    mem_GLOBAL.imprimirDir()
    terminado = False # nos avisas cuando salir del programa
    while not terminado:
        sigCuaIndice = -1 # nos permite llevar control, de que cuadro ejecutar
        pilaCorriendo = top(CONST_EJECUCION) # Saca la instancia de memoria que se este ejecutando
        cuadruplo = cuaLista[cuaIndice] # Saca el cuadruplo a ejecutar

        # ASIGNACION
        if cuadruplo[0] == '=':
            try: # Sino encuentra el valor, checa que este en la pila de valores de retorno 
                valor = getValor(pilaCorriendo, cuadruplo[1], getTipo(cuadruplo[1]))
            except:
                valor = pop(CONST_RETORNO_VALOR)
                
            llenarValor(pilaCorriendo, cuadruplo[3], getTipo(cuadruplo[3]), valor)
        # COMANDOS        
        # CONS
        # Se saltará porque ya se agregarón con antelación
        # GOTO
        elif cuadruplo[0] == 'GOTO':
            #print("Ejecutando GOTO: ", cuadruplo)
            sigCuaIndice = int(cuadruplo[3])
        # GOTOF
        elif cuadruplo[0] == 'GOTOF':
            #print("Ejecutando GOTOF: ", cuadruplo)
            auxValor = getValor(pilaCorriendo, cuadruplo[1], getTipo(cuadruplo[1]))
            if not auxValor: #Confirma si es falso el valor
                sigCuaIndice = int(cuadruplo[3])
        # GOSUB
        elif cuadruplo[0] == 'GOSUB':
            #print("CAMBIO DE CONTEXTO A FUNCION: ")
            pilaCorriendo = pop(CONST_TEMPORAL) # Sacamos la instancia de memoria temporal
            push(CONST_EJECUCION, pilaCorriendo) # Metemos la instancia a ejecucion
            push(CONST_FUNCION_RETORNO, cuadruplo[2]) # Guardamos el retorno
            sigCuaIndice = int(cuadruplo[3])
        # ERA
        elif cuadruplo[0] == 'ERA':
            #Declara nueva funcion de memoria virtual
            #print("CREANDO MEMORIA DE FUNCION: ")
            memNueva = memoriaVirtual(str(cuadruplo[1]))
            #memNueva.imprimirDir()
            push(CONST_TEMPORAL, memNueva)
        # PARAMETER
        elif cuadruplo[0] == 'PARAMETER':
            tipo = getTipo(cuadruplo[1])
            valor = getValor(pilaCorriendo, cuadruplo[1], tipo)
            auxMem = top(CONST_TEMPORAL)
            # Nos permite saber que direccion sigue
            # Donde empiezan las variables globales 
            direccion = auxMem.sigDireccionDisponible(tipo, 4000, ESPACIO_MEMORIA)
            llenarValor(auxMem, direccion, getTipo(direccion), valor)
            #print("INSERTANDO PARAMETRO A LA MEMORIA DE FUNCION: ")
            #auxMem.imprimirDir()
        # ENDFUNC
        elif cuadruplo[0] == 'ENDFUNC':
            #print("FIN DE FUNCION")
            pop(CONST_EJECUCION)
            sigCuaIndice = int(pop(CONST_FUNCION_RETORNO))
        # regresa
        elif cuadruplo[0] == 'regresa':
            valor = getValor(pilaCorriendo, cuadruplo[3], getTipo(cuadruplo[3]))
            push(CONST_RETORNO_VALOR, str(valor)) #Guarda el valor para despues
            pop(CONST_EJECUCION) #Sacar funcion de la pila, porque se termino de ejecutar
            sigCuaIndice = int(pop(CONST_FUNCION_RETORNO))
        # lee
        elif cuadruplo[0] == 'lee':
            texto = input("<- ")
            #Verifica que tipo de valor es el que recibe, para guardarlo donde corresponde
            try:
                int(texto)
                tipo = 'entero'
            except:
                try:
                    float(texto)
                    tipo = 'flotante'
                except:
                    try:
                        str(texto)
                        tipo = 'char' if len(texto) == 1 else 'string'
                    except:
                        print("Error Maquina Virtual: {}".format(sys.exc_info()[0], cuaIndice))
            auxTipo = getTipo(cuadruplo[1])
            if tipo == 'entero' and auxTipo == 'flotante':
                llenarValor(pilaCorriendo,cuadruplo[1],auxTipo,int(texto))
            elif tipo == 'flotante' and auxTipo == 'entero':
                llenarValor(pilaCorriendo,cuadruplo[1],auxTipo,float(texto))
            elif tipo == auxTipo:
                llenarValor(pilaCorriendo, cuadruplo[1], auxTipo, texto)
            else:
                print("Error Maquina Virtual: {} es diferente a {}".format(tipo, auxTipo))
                sys.exit()
                return
        # escribe
        elif cuadruplo[0] == 'escribe':
            #Trae el valor y lo imprime
            texto = getValor(pilaCorriendo, cuadruplo[1], getTipo(cuadruplo[1]))
            print("->",str(texto))
        #dibuja linea
        elif cuadruplo[0] == 'linea':
            numero = getValor(pilaCorriendo,cuadruplo[1], getTipo(cuadruplo[1]))
            if cuadruplo[3] == 'fd':
                fd(int(numero))
            elif cuadruplo[3] == 'bk':
                bk(int(numero))
            elif cuadruplo[3] == 'rt':
                rt(int(numero))
            elif cuadruplo[3] == 'lt':
                lt(int(numero))
        #penup
        elif cuadruplo[0] == 'penup':
            pen_up()
        #pendown
        elif cuadruplo[0] == 'pendown':
            pen_down()
        #limpiar
        elif cuadruplo[0] == 'limpiar':
            clear_screen()
        #punto
        elif cuadruplo[0] == 'punto':
            y = getValor(pilaCorriendo,cuadruplo[1],getTipo(cuadruplo[1]))
            x = getValor(pilaCorriendo, cuadruplo[2],getTipo(cuadruplo[2]))
            setxy(int(x),int(y))
        #circulo
        elif cuadruplo[0] == 'circulo':
            x = get_x()
            y = get_y()
            r = getValor(pilaCorriendo, cuadruplo[1], getTipo(cuadruplo[1]))
            circle(int(x),int(y),int(r))
        #grosor
        elif cuadruplo[0] == 'grosor':
            grosor = getValor(pilaCorriendo, cuadruplo[1], getTipo(cuadruplo[1]))
            set_line_width(int(grosor))
        elif cuadruplo[0] == 'arco':
            x = get_x()
            y = get_y()
            radio_x = getValor(pilaCorriendo, cuadruplo[2],getTipo(cuadruplo[2]))
            radio_y = getValor(pilaCorriendo,cuadruplo[1],getTipo(cuadruplo[1]))
            start_angle = 0
            end_angle = 180
            draw_arc(x,y,start_angle,end_angle,int(radio_x),int(radio_y))

        #FINPROGRAMA
        elif cuadruplo[0] == 'FINPROGRAMA':
            print("FIN PROGRAMA")
            terminado = True
        # OPERADORES 
        elif cuadruplo[0] != 'CONS':
            operadores(cuadruplo[0])

        # Controla el indice para saber que cuadroplo ejecutar
        if sigCuaIndice != -1:
            cuaIndice = sigCuaIndice
        else: 
            cuaIndice = cuaIndice + 1

# Funcion para abrir archivo
def getArchivo(name):
    try:
        f = open(name,'r', encoding='utf-8')
        return f
    except EOFError:
        print ("Error Maquina Virtual:", EOFError, " no se encuentra el archivo {}".format(name))


cuadruplos = getArchivo('obj.txt') # saca el archivo de cuadruplos
# GUarda los cuadruplos en una lista
for linea in cuadruplos:
    linea = linea.replace('(','')
    linea = linea.replace(')','')
    linea = linea.replace('\n','')
    linea = linea.replace('\'','')
    linea = linea.replace(' ','')
    cuadruplo = tuple(linea.split(','))
    if (cuadruplo[0] == 'CONS'): # Lista de constntes, para guardarlos desde un principio en memoria
        cuadroCONST = (cuadruplo[0], cuadruplo[1], cuadruplo[2], cuadruplo[3])
        constLista.append(cuadroCONST)
    cuadruplo = (cuadruplo[0], cuadruplo[1], cuadruplo[2], cuadruplo[3])
    cuaLista.append(cuadruplo)
print(constLista)

easy_run(main)


