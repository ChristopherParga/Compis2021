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
            ('int' , 'int' , '+' ) : 'int',
            ('int' , 'int' , '-' ) : 'int',
            ('int' , 'int' , '*' ) : 'int',
            ('int' , 'int' , '/' ) : 'int',
            ('int' , 'int' , '=' ) : 'int',
            ('int' , 'int' , '==' ) : 'bool',
            ('int' , 'int' , '<' ) : 'bool',
            ('int' , 'int' , '>' ) : 'bool',
            ('int' , 'int' , '<=' ) : 'bool',
            ('int' , 'int' , '>=' ) : 'bool',
            ('int' , 'int' , '!=' ) : 'bool',
            ('int' , 'int' , '|' ) : 'error',
            ('int' , 'int' , '&' ) : 'error',

            ('int' , 'float' , '+' ) : 'float',
            ('int' , 'float' , '-' ) : 'float',
            ('int' , 'float' , '*' ) : 'float',
            ('int' , 'float' , '/' ) : 'float',
            ('int' , 'float' , '=' ) : 'int',
            ('int' , 'float' , '==' ) : 'bool',
            ('int' , 'float' , '<' ) : 'bool',
            ('int' , 'float' , '>' ) : 'bool',
            ('int' , 'float' , '<=' ) : 'bool',
            ('int' , 'float' , '>=' ) : 'bool',
            ('int' , 'float' , '!=' ) : 'bool',
            ('int' , 'float' , '|' ) : 'error',
            ('int' , 'float' , '&' ) : 'error',

            ('int' , 'char' , '+' ) : 'error',
            ('int' , 'char' , '-' ) : 'error',
            ('int' , 'char' , '*' ) : 'error',
            ('int' , 'char' , '/' ) : 'error',
            ('int' , 'char' , '=' ) : 'error', 
            ('int' , 'char' , '==' ) : 'error',
            ('int' , 'char' , '<' ) : 'error',
            ('int' , 'char' , '>' ) : 'error',
            ('int' , 'char' , '<=' ) : 'error',
            ('int' , 'char' , '>=' ) : 'error',
            ('int' , 'char' , '!=' ) : 'error',
            ('int' , 'char' , '|' ) : 'error',
            ('int' , 'char' , '&' ) : 'error',
 
            ('int' , 'array' , '+' ) : 'error',
            ('int' , 'array' , '-' ) : 'error',
            ('int' , 'array' , '*' ) : 'error',
            ('int' , 'array' , '/' ) : 'error',
            ('int' , 'array' , '=' ) : 'error', 
            ('int' , 'array' , '==' ) : 'error',
            ('int' , 'array' , '<' ) : 'error',
            ('int' , 'array' , '>' ) : 'error',
            ('int' , 'array' , '<=' ) : 'error',
            ('int' , 'array' , '>=' ) : 'error',
            ('int' , 'array' , '!=' ) : 'error',
            ('int' , 'array' , '|' ) : 'error',
            ('int' , 'array' , '&' ) : 'error',
            
            #Float 
            ('float' , 'int' , '+' ) : 'float',
            ('float' , 'int' , '-' ) : 'float',
            ('float' , 'int' , '*' ) : 'float',
            ('float' , 'int' , '/' ) : 'float',
            ('float' , 'int' , '=' ) : 'float', 
            ('float' , 'int' , '==' ) : 'bool',
            ('float' , 'int' , '<' ) : 'bool',
            ('float' , 'int' , '>' ) : 'bool',
            ('float' , 'int' , '<=' ) : 'bool',
            ('float' , 'int' , '>=' ) : 'bool',
            ('float' , 'int' , '!=' ) : 'bool',
            ('float' , 'int' , '|' ) : 'error',
            ('float' , 'int' , '&' ) : 'error',

            ('float' , 'float' , '+' ) : 'float',
            ('float' , 'float' , '-' ) : 'float',
            ('float' , 'float' , '*' ) : 'float',
            ('float' , 'float' , '/' ) : 'float',
            ('float' , 'float' , '=' ) : 'float', 
            ('float' , 'float' , '==' ) : 'bool',
            ('float' , 'float' , '<' ) : 'bool',
            ('float' , 'float' , '>' ) : 'bool',
            ('float' , 'float' , '<=' ) : 'bool',
            ('float' , 'float' , '>=' ) : 'bool',
            ('float' , 'float' , '!=' ) : 'bool',
            ('float' , 'float' , '|' ) : 'error',
            ('float' , 'float' , '&' ) : 'error',

            ('float' , 'char' , '+' ) : 'error',
            ('float' , 'char' , '-' ) : 'error',
            ('float' , 'char' , '*' ) : 'error',
            ('float' , 'char' , '/' ) : 'error',
            ('float' , 'char' , '=' ) : 'error', 
            ('float' , 'char' , '==' ) : 'error',
            ('float' , 'char' , '<' ) : 'error',
            ('float' , 'char' , '>' ) : 'error',
            ('float' , 'char' , '<=' ) : 'error',
            ('float' , 'char' , '>=' ) : 'error',
            ('float' , 'char' , '!=' ) : 'error',
            ('float' , 'char' , '|' ) : 'error',
            ('float' , 'char' , '&' ) : 'error',


            ('float' , 'array' , '+' ) : 'error',
            ('float' , 'array' , '-' ) : 'error',
            ('float' , 'array' , '*' ) : 'error',
            ('float' , 'array' , '/' ) : 'error',
            ('float' , 'array' , '=' ) : 'error', 
            ('float' , 'array' , '==' ) : 'error',
            ('float' , 'array' , '<' ) : 'error',
            ('float' , 'array' , '>' ) : 'error',
            ('float' , 'array' , '<=' ) : 'error',
            ('float' , 'array' , '>=' ) : 'error',
            ('float' , 'array' , '!=' ) : 'error',
            ('float' , 'array' , '|' ) : 'error',
            ('float' , 'array' , '&' ) : 'error',

            #Char
            ('char' , 'int' , '+' ) : 'error',
            ('char' , 'int' , '-' ) : 'error',
            ('char' , 'int' , '*' ) : 'error',
            ('char' , 'int' , '/' ) : 'error',
            ('char' , 'int' , '=' ) : 'error', 
            ('char' , 'int' , '==' ) : 'error',
            ('char' , 'int' , '<' ) : 'error',
            ('char' , 'int' , '>' ) : 'error',
            ('char' , 'int' , '<=' ) : 'error',
            ('char' , 'int' , '>=' ) : 'error',
            ('char' , 'int' , '!=' ) : 'error',
            ('char' , 'int' , '|' ) : 'error',
            ('char' , 'int' , '&' ) : 'error',

            ('char' , 'float' , '+' ) : 'error',
            ('char' , 'float' , '-' ) : 'error',
            ('char' , 'float' , '*' ) : 'error',
            ('char' , 'float' , '/' ) : 'error',
            ('char' , 'float' , '=' ) : 'error', 
            ('char' , 'float' , '==' ) : 'error',
            ('char' , 'float' , '<' ) : 'error',
            ('char' , 'float' , '>' ) : 'error',
            ('char' , 'float' , '<=' ) : 'error',
            ('char' , 'float' , '>=' ) : 'error',
            ('char' , 'float' , '!=' ) : 'error',
            ('char' , 'float' , '|' ) : 'error',
            ('char' , 'float' , '&' ) : 'error',

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
            ('array' , 'int' , '+' ) : 'error',
            ('array' , 'int' , '-' ) : 'error',
            ('array' , 'int' , '*' ) : 'error',
            ('array' , 'int' , '/' ) : 'error',
            ('array' , 'int' , '=' ) : 'error', 
            ('array' , 'int' , '==' ) : 'error',
            ('array' , 'int' , '<' ) : 'error',
            ('array' , 'int' , '>' ) : 'error',
            ('array' , 'int' , '<=' ) : 'error',
            ('array' , 'int' , '>=' ) : 'error',
            ('array' , 'int' , '!=' ) : 'error',
            ('array' , 'int' , '|' ) : 'error',
            ('array' , 'int' , '&' ) : 'error',

            ('array' , 'float' , '+' ) : 'error',
            ('array' , 'float' , '-' ) : 'error',
            ('array' , 'float' , '*' ) : 'error',
            ('array' , 'float' , '/' ) : 'error',
            ('array' , 'float' , '=' ) : 'error', 
            ('array' , 'float' , '==' ) : 'error',
            ('array' , 'float' , '<' ) : 'error',
            ('array' , 'float' , '>' ) : 'error',
            ('array' , 'float' , '<=' ) : 'error',
            ('array' , 'float' , '>=' ) : 'error',
            ('array' , 'float' , '!=' ) : 'error',
            ('array' , 'float' , '|' ) : 'error',
            ('array' , 'float' , '&' ) : 'error',

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
            ('lee', 'int', '') : 'int',
            ('lee', 'float', '') : 'float',
            ('lee', 'char', '') : 'error',
            ('lee', 'string', '') : 'error',
            ('lee', 'array', '') : 'char', #?????

            #Escritura
            ('escribe', 'int', '') : 'string',
            ('escribe', 'float', '') : 'string',
            ('escribe', 'char', '') : 'string',
            ('escribe', 'string', '') : 'string',
            ('escribe', 'array', '') : 'error',

            #Retorno
            ('regresa', 'int', '') : 'int',
            ('regresa', 'float', '') : 'float',
            ('regresa', 'char', '') : 'char',
            ('regresa', 'string', '') : 'string',
            ('regresa', 'array', '') : 'array'
        }

    '''
    Funcion para obtener el TIPO DE RESULTADO de la operacion con el operador entre dos operandos
    '''
    def getType(self, operando1, operando2, operador):
        return self.CuboSem[operando1, operando2, operador]
