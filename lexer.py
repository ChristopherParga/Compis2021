import ply.lex as lex
#Lista de Tokens para el lenguaje
tokens = [
    #palabras reservadas
    'PROGRAMA','VOID','PRINCIPAL','ID','COMMENT',
    'ESCRIBE','LEE','REGRESA','SI','ENTONCES','SINO','MIENTRAS',
    'VARIABLES', 'FUNCION', 'HACER', 'DESDE', 'HASTA',
    #tipos de datos
    'INT_TYPE','FLOAT_TYPE','CHAR_TYPE',
    #asignacion
    'ASSIGN',
    #operadores aritmeticos
    'PLUS_OP','MINUS_OP','MULT_OP','DIV_OP',
    #operadores logicos
    'EQUAL_LOG','LT_LOG','LTE_LOG','GT_LOG',
    'GTE_LOG','NE_LOG','OR_LOG','AND_LOG',
    #simbolos para conjuntos y scope
    'LPAREN','RPAREN','LBRACK','RBRACK','LCURLY','RCURLY',
    #operadores especiales
    'COMMA','SEMIC','COLON',
    #constantes
    'FLOAT_CTE','INT_CTE','CHAR_CTE','STRING_CTE',
    'NEW_LINE'
]

#Expresiones Regulares para tokens
t_PLUS_OP = r'\+'
t_MINUS_OP = r'-'
t_MULT_OP = r'\*'
t_DIV_OP = r'/'
t_ASSIGN = r'\='
t_EQUAL_LOG = r'\=\='
t_LT_LOG = r'\<'
t_LTE_LOG = r'\<\='
t_GT_LOG = r'\>'
t_GTE_LOG = r'\>\='
t_NE_LOG = r'\!\='
t_OR_LOG = r'\|'
t_AND_LOG = r'\&'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_LCURLY = r'\{'
t_RCURLY = r'\}'
t_COMMA = r'\,'
t_SEMIC = r'\;'
t_COLON = r'\:'
t_ignore = ' \t\n'



def t_FLOAT_CTE(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT_CTE(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CHAR_CTE(t):
    r'(\"([^\\\"]|\\.)+\")|(\'([^\\\']|\\.)+\')'
    t.value = str(t.value)
    return t

def t_COMMENT(t):
    r'\%\%'
    pass


def t_NEW_LINE(t):
    r'\n'
    t.lexer.lineno += 1
    pass

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value == 'programa':
        t.type = 'PROGRAMA'
    elif t.value == 'void':
        t.type = 'VOID'
    elif t.value == 'principal':
        t.type = 'PRINCIPAL'
    elif t.value == 'funcion':
        t.type = 'FUNCION'
    elif t.value == 'escribe':
        t.type = 'ESCRIBE'
    elif t.value == 'lee':
        t.type = 'LEE'
    elif t.value == 'si':
        t.type = 'SI'
    elif t.value == 'entonces':
        t.type = 'ENTONCES'
    elif t.value == 'sino':
        t.type = 'SINO'    
    elif t.value == 'mientras':
        t.type = 'MIENTRAS'
    elif t.value == 'hacer':
        t.type = 'HACER'
    elif t.value == 'desde':
        t.type = 'DESDE'
    elif t.value == 'hasta':
        t.type = 'HASTA'
    elif t.value == 'entero':
        t.type = 'INT_TYPE'
    elif t.value == 'flotante':
        t.type = 'FLOAT_TYPE'
    elif t.value == 'char':
        t.type = 'CHAR_TYPE'
    elif t.value == 'variables':
        t.type = 'VARIABLES'
    else:
        t.type = 'ID'
    return t

#Error generico
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    print(t.token)
    t.lexer.skip(1)


while True:
    tok = lexer.token()
    if not tok : break
    print(tok)