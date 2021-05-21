import sys
"""
Esta clase permitirá manejar la memoria de la maquina virtual,
mediante instancias, que seran generadas para cada funcion recibida,
empezando por la global. 
"""

class memoriaVirtual:
    def __init__(self, fun):
        # Guardamos el nombre de funcion al que pertenece la tabla
        self.funNombre = fun
        # Declaramos diccionario para las direcciones de valores constantes
        self.direcciones = {
            #tipo       #direcciones : valor
            'entero'       : {},
            'flotante'     : {},
            'char'      : {},
            'string'    : {},
            'bool'      : {},
        }

    """
    Guardar el valor, en una direccion específica
    """
    def guardarValor(self, direccion, tipo, valor):
        self.direcciones[str(tipo)][str(direccion)] = valor

    """
    Obtener el valor de una direccion en específico
    """
    def obtenerValorDeDireccion(self, direccion, tipo):
        #print('direccion: ', direccion)
        #print('tipo: ', tipo)
        try:
            valor = self.direcciones[str(tipo)][str(direccion)]
            return valor
        except:
            print("Error Memoria Virtual: ", sys.exc_info()[0], "No existe valor, en memoria {} en la direccion {}, de tipo {}.".format( self.funNombre, direccion, tipo))
            raise

    """
    Obtener la siguiente dirreccion disponible
    """
    def sigDireccionDisponible(self, tipo, direccion_inicial, tam):
        if tipo == 'entero':
            aux = 0
        elif tipo == 'flotante':
            aux = tam
        elif tipo == 'char':
            aux = tam * 2
        elif tipo == 'string':
            aux = tam * 3

        return direccion_inicial + aux + len(self.direcciones[tipo])

    """
    Imprimir diccionario de la memoria
    """
    def imprimirDir(self):
        print("Nombre {}: ".format(self.funNombre))
        print(self.direcciones)
        print("\n")