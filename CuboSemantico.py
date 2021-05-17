'''
Para representar el cubo semantico vamos a utilizar un Diccionario que contiene todas las combinaciones posibles entre dos operandos, utilizando todos los tipos que existen en el lenguaje COVID. 
        
Los tipos de datos que contiene COVID son:
    - Int
    - Float
    - Char
    - Array

Tambien incluye los resultados cuando se utilizan los estatutos de lectura (lee) y escritura (escribe). 

La estructura que va a manejar el cubo semantico es la siguiente:
        
    (operando1, operando2, operador) : tipo de operando resultante

    Error: Type Mismatch
        
'''
class CuboSemantico:

    ''' 
    Conctructor
    '''
    def __init__(self):

        self.CuboSem = {
            #Int 
            ('entero' , 'entero' , '+' ) : 'entero',
            ('entero' , 'entero' , '-' ) : 'entero',
            ('entero' , 'entero' , '*' ) : 'entero',
            ('entero' , 'entero' , '/' ) : 'entero',
            ('entero' , 'entero' , '=' ) : 'entero',
            ('entero' , 'entero' , '==' ) : 'bool',
            ('entero' , 'entero' , '<' ) : 'bool',
            ('entero' , 'entero' , '>' ) : 'bool',
            ('entero' , 'entero' , '<=' ) : 'bool',
            ('entero' , 'entero' , '>=' ) : 'bool',
            ('entero' , 'entero' , '!=' ) : 'bool',
            ('entero' , 'entero' , '|' ) : 'error',
            ('entero' , 'entero' , '&' ) : 'error',

            ('entero' , 'flotante' , '+' ) : 'flotante',
            ('entero' , 'flotante' , '-' ) : 'flotante',
            ('entero' , 'flotante' , '*' ) : 'flotante',
            ('entero' , 'flotante' , '/' ) : 'flotante',
            ('entero' , 'flotante' , '=' ) : 'entero',
            ('entero' , 'flotante' , '==' ) : 'bool',
            ('entero' , 'flotante' , '<' ) : 'bool',
            ('entero' , 'flotante' , '>' ) : 'bool',
            ('entero' , 'flotante' , '<=' ) : 'bool',
            ('entero' , 'flotante' , '>=' ) : 'bool',
            ('entero' , 'flotante' , '!=' ) : 'bool',
            ('entero' , 'flotante' , '|' ) : 'error',
            ('entero' , 'flotante' , '&' ) : 'error',

            ('entero' , 'char' , '+' ) : 'error',
            ('entero' , 'char' , '-' ) : 'error',
            ('entero' , 'char' , '*' ) : 'error',
            ('entero' , 'char' , '/' ) : 'error',
            ('entero' , 'char' , '=' ) : 'error', 
            ('entero' , 'char' , '==' ) : 'error',
            ('entero' , 'char' , '<' ) : 'error',
            ('entero' , 'char' , '>' ) : 'error',
            ('entero' , 'char' , '<=' ) : 'error',
            ('entero' , 'char' , '>=' ) : 'error',
            ('entero' , 'char' , '!=' ) : 'error',
            ('entero' , 'char' , '|' ) : 'error',
            ('entero' , 'char' , '&' ) : 'error',
 
            ('entero' , 'array' , '+' ) : 'error',
            ('entero' , 'array' , '-' ) : 'error',
            ('entero' , 'array' , '*' ) : 'error',
            ('entero' , 'array' , '/' ) : 'error',
            ('entero' , 'array' , '=' ) : 'error', 
            ('entero' , 'array' , '==' ) : 'error',
            ('entero' , 'array' , '<' ) : 'error',
            ('entero' , 'array' , '>' ) : 'error',
            ('entero' , 'array' , '<=' ) : 'error',
            ('entero' , 'array' , '>=' ) : 'error',
            ('entero' , 'array' , '!=' ) : 'error',
            ('entero' , 'array' , '|' ) : 'error',
            ('entero' , 'array' , '&' ) : 'error',
            
            #Float 
            ('flotante' , 'entero' , '+' ) : 'flotante',
            ('flotante' , 'entero' , '-' ) : 'flotante',
            ('flotante' , 'entero' , '*' ) : 'flotante',
            ('flotante' , 'entero' , '/' ) : 'flotante',
            ('flotante' , 'entero' , '=' ) : 'flotante', 
            ('flotante' , 'entero' , '==' ) : 'bool',
            ('flotante' , 'entero' , '<' ) : 'bool',
            ('flotante' , 'entero' , '>' ) : 'bool',
            ('flotante' , 'entero' , '<=' ) : 'bool',
            ('flotante' , 'entero' , '>=' ) : 'bool',
            ('flotante' , 'entero' , '!=' ) : 'bool',
            ('flotante' , 'entero' , '|' ) : 'error',
            ('flotante' , 'entero' , '&' ) : 'error',

            ('flotante' , 'flotante' , '+' ) : 'flotante',
            ('flotante' , 'flotante' , '-' ) : 'flotante',
            ('flotante' , 'flotante' , '*' ) : 'flotante',
            ('flotante' , 'flotante' , '/' ) : 'flotante',
            ('flotante' , 'flotante' , '=' ) : 'flotante', 
            ('flotante' , 'flotante' , '==' ) : 'bool',
            ('flotante' , 'flotante' , '<' ) : 'bool',
            ('flotante' , 'flotante' , '>' ) : 'bool',
            ('flotante' , 'flotante' , '<=' ) : 'bool',
            ('flotante' , 'flotante' , '>=' ) : 'bool',
            ('flotante' , 'flotante' , '!=' ) : 'bool',
            ('flotante' , 'flotante' , '|' ) : 'error',
            ('flotante' , 'flotante' , '&' ) : 'error',

            ('flotante' , 'char' , '+' ) : 'error',
            ('flotante' , 'char' , '-' ) : 'error',
            ('flotante' , 'char' , '*' ) : 'error',
            ('flotante' , 'char' , '/' ) : 'error',
            ('flotante' , 'char' , '=' ) : 'error', 
            ('flotante' , 'char' , '==' ) : 'error',
            ('flotante' , 'char' , '<' ) : 'error',
            ('flotante' , 'char' , '>' ) : 'error',
            ('flotante' , 'char' , '<=' ) : 'error',
            ('flotante' , 'char' , '>=' ) : 'error',
            ('flotante' , 'char' , '!=' ) : 'error',
            ('flotante' , 'char' , '|' ) : 'error',
            ('flotante' , 'char' , '&' ) : 'error',


            ('flotante' , 'array' , '+' ) : 'error',
            ('flotante' , 'array' , '-' ) : 'error',
            ('flotante' , 'array' , '*' ) : 'error',
            ('flotante' , 'array' , '/' ) : 'error',
            ('flotante' , 'array' , '=' ) : 'error', 
            ('flotante' , 'array' , '==' ) : 'error',
            ('flotante' , 'array' , '<' ) : 'error',
            ('flotante' , 'array' , '>' ) : 'error',
            ('flotante' , 'array' , '<=' ) : 'error',
            ('flotante' , 'array' , '>=' ) : 'error',
            ('flotante' , 'array' , '!=' ) : 'error',
            ('flotante' , 'array' , '|' ) : 'error',
            ('flotante' , 'array' , '&' ) : 'error',

            #Char
            ('char' , 'entero' , '+' ) : 'error',
            ('char' , 'entero' , '-' ) : 'error',
            ('char' , 'entero' , '*' ) : 'error',
            ('char' , 'entero' , '/' ) : 'error',
            ('char' , 'entero' , '=' ) : 'error', 
            ('char' , 'entero' , '==' ) : 'error',
            ('char' , 'entero' , '<' ) : 'error',
            ('char' , 'entero' , '>' ) : 'error',
            ('char' , 'entero' , '<=' ) : 'error',
            ('char' , 'entero' , '>=' ) : 'error',
            ('char' , 'entero' , '!=' ) : 'error',
            ('char' , 'entero' , '|' ) : 'error',
            ('char' , 'entero' , '&' ) : 'error',

            ('char' , 'flotante' , '+' ) : 'error',
            ('char' , 'flotante' , '-' ) : 'error',
            ('char' , 'flotante' , '*' ) : 'error',
            ('char' , 'flotante' , '/' ) : 'error',
            ('char' , 'flotante' , '=' ) : 'error', 
            ('char' , 'flotante' , '==' ) : 'error',
            ('char' , 'flotante' , '<' ) : 'error',
            ('char' , 'flotante' , '>' ) : 'error',
            ('char' , 'flotante' , '<=' ) : 'error',
            ('char' , 'flotante' , '>=' ) : 'error',
            ('char' , 'flotante' , '!=' ) : 'error',
            ('char' , 'flotante' , '|' ) : 'error',
            ('char' , 'flotante' , '&' ) : 'error',

            ('char' , 'char' , '+' ) : 'error',
            ('char' , 'char' , '-' ) : 'error',
            ('char' , 'char' , '*' ) : 'error',
            ('char' , 'char' , '/' ) : 'error',
            ('char' , 'char' , '=' ) : 'char', 
            ('char' , 'char' , '==' ) : 'bool',
            ('char' , 'char' , '<' ) : 'error',
            ('char' , 'char' , '>' ) : 'error',
            ('char' , 'char' , '<=' ) : 'error',
            ('char' , 'char' , '>=' ) : 'error',
            ('char' , 'char' , '!=' ) : 'bool',
            ('char' , 'char' , '|' ) : 'error',
            ('char' , 'char' , '&' ) : 'error',

            ('char' , 'array' , '+' ) : 'error',
            ('char' , 'array' , '-' ) : 'error',
            ('char' , 'array' , '*' ) : 'error',
            ('char' , 'array' , '/' ) : 'error',
            ('char' , 'array' , '=' ) : 'error', 
            ('char' , 'array' , '==' ) : 'error',
            ('char' , 'array' , '<' ) : 'error',
            ('char' , 'array' , '>' ) : 'error',
            ('char' , 'array' , '<=' ) : 'error',
            ('char' , 'array' , '>=' ) : 'error',
            ('char' , 'array' , '!=' ) : 'error',
            ('char' , 'array' , '|' ) : 'error',
            ('char' , 'array' , '&' ) : 'error',

            #array
            ('array' , 'entero' , '+' ) : 'error',
            ('array' , 'entero' , '-' ) : 'error',
            ('array' , 'entero' , '*' ) : 'error',
            ('array' , 'entero' , '/' ) : 'error',
            ('array' , 'entero' , '=' ) : 'error', 
            ('array' , 'entero' , '==' ) : 'error',
            ('array' , 'entero' , '<' ) : 'error',
            ('array' , 'entero' , '>' ) : 'error',
            ('array' , 'entero' , '<=' ) : 'error',
            ('array' , 'entero' , '>=' ) : 'error',
            ('array' , 'entero' , '!=' ) : 'error',
            ('array' , 'entero' , '|' ) : 'error',
            ('array' , 'entero' , '&' ) : 'error',

            ('array' , 'flotante' , '+' ) : 'error',
            ('array' , 'flotante' , '-' ) : 'error',
            ('array' , 'flotante' , '*' ) : 'error',
            ('array' , 'flotante' , '/' ) : 'error',
            ('array' , 'flotante' , '=' ) : 'error', 
            ('array' , 'flotante' , '==' ) : 'error',
            ('array' , 'flotante' , '<' ) : 'error',
            ('array' , 'flotante' , '>' ) : 'error',
            ('array' , 'flotante' , '<=' ) : 'error',
            ('array' , 'flotante' , '>=' ) : 'error',
            ('array' , 'flotante' , '!=' ) : 'error',
            ('array' , 'flotante' , '|' ) : 'error',
            ('array' , 'flotante' , '&' ) : 'error',

            ('array' , 'char' , '+' ) : 'error',
            ('array' , 'char' , '-' ) : 'error',
            ('array' , 'char' , '*' ) : 'error',
            ('array' , 'char' , '/' ) : 'error',
            ('array' , 'char' , '=' ) : 'error', 
            ('array' , 'char' , '==' ) : 'error',
            ('array' , 'char' , '<' ) : 'error',
            ('array' , 'char' , '>' ) : 'error',
            ('array' , 'char' , '<=' ) : 'error',
            ('array' , 'char' , '>=' ) : 'error',
            ('array' , 'char' , '!=' ) : 'error',
            ('array' , 'char' , '|' ) : 'error',
            ('array' , 'char' , '&' ) : 'error',

            ('array' , 'string' , '+' ) : 'error',
            ('array' , 'string' , '-' ) : 'error',
            ('array' , 'string' , '*' ) : 'error',
            ('array' , 'string' , '/' ) : 'error',
            ('array' , 'string' , '=' ) : 'error', 
            ('array' , 'string' , '==' ) : 'error',
            ('array' , 'string' , '<' ) : 'error',
            ('array' , 'string' , '>' ) : 'error',
            ('array' , 'string' , '<=' ) : 'error',
            ('array' , 'string' , '>=' ) : 'error',
            ('array' , 'string' , '!=' ) : 'error',
            ('array' , 'string' , '|' ) : 'error',
            ('array' , 'string' , '&' ) : 'error',

            ('array' , 'array' , '+' ) : 'error',
            ('array' , 'array' , '-' ) : 'error',
            ('array' , 'array' , '*' ) : 'error',
            ('array' , 'array' , '/' ) : 'error',
            ('array' , 'array' , '=' ) : 'array', 
            ('array' , 'array' , '==' ) : 'error',
            ('array' , 'array' , '<' ) : 'error',
            ('array' , 'array' , '>' ) : 'error',
            ('array' , 'array' , '<=' ) : 'error',
            ('array' , 'array' , '>=' ) : 'error',
            ('array' , 'array' , '!=' ) : 'error',
            ('array' , 'array' , '|' ) : 'error',
            ('array' , 'array' , '&' ) : 'error',

            #Lectura
            ('lee', 'entero', '') : 'entero',
            ('lee', 'flotante', '') : 'flotante',
            ('lee', 'char', '') : 'error',
            ('lee', 'string', '') : 'error',
            ('lee', 'array', '') : 'char', #?????

            #Escritura
            ('escribe', 'entero', '') : 'string',
            ('escribe', 'flotante', '') : 'string',
            ('escribe', 'char', '') : 'string',
            ('escribe', 'string', '') : 'string',
            ('escribe', 'array', '') : 'error',

            #Retorno
            ('regresa', 'entero', '') : 'entero',
            ('regresa', 'flotante', '') : 'flotante',
            ('regresa', 'char', '') : 'char',
            ('regresa', 'string', '') : 'string',
            ('regresa', 'array', '') : 'array'
        }

    '''
    Funcion para obtener el TIPO DE RESULTADO de la operacion con el operador entre dos operandos
    '''
    def getType(self, operando1, operando2, operador):
        return self.CuboSem[operando1, operando2, operador]
