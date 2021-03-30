import ply.lex as lex
#Lista de Tokens para el lenguaje
tokens = [
    #palabras reservadas
    'PROGRAM','VOID','MAIN','ID','COMMENT',
    'WRITE','READ','RETURN','IF','ELSE','WHILE',
    'VAR', 'MODULE', 'DO', 'FOR', 'TO',
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
    #funciones especiales
    'LINE','POINT','CIRCLE','ARC','PENUP',
    'PENDOWN','COLOR','SIZE','CLEAR',
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
    if t.value == 'program':
        t.type = 'PROGRAM'
    elif t.value == 'void':
        t.type = 'VOID'
    elif t.value == 'main':
        t.type = 'MAIN'
    elif t.value == 'func':
        t.type = 'FUNC'
    elif t.value == 'write':
        t.type = 'WRITE'
    elif t.value == 'read':
        t.type = 'READ'
    elif t.value == 'if':
        t.type = 'IF'
    elif t.value == 'else':
        t.type = 'ELSE'
    elif t.value == 'while':
        t.type = 'WHILE'
    elif t.value == 'do':
        t.type = 'DO'
    elif t.value == 'for':
        t.type = 'FOR'
    elif t.value == 'to':
        t.type = 'TO'
    elif t.value == 'int':
        t.type = 'INT_TYPE'
    elif t.value == 'float':
        t.type = 'FLOAT_TYPE'
    elif t.value == 'char':
        t.type = 'CHAR_TYPE'
    elif t.value == 'var':
        t.type = 'VAR'
    elif t.value == 'line':
        t.type = 'LINE'
    elif t.value == 'point':
        t.type = 'POINT'
    elif t.value == 'circle':
        t.type = 'CIRCLE'
    elif t.value == 'arc':
        t.type = 'ARC'
    elif t.value == 'penup':
        t.type = 'PENUP'
    elif t.value == 'pendown':
        t.type = 'PENDOWN'
    elif t.value == 'color':
        t.type = 'COLOR'
    elif t.value == 'size':
        t.type = 'SIZE'
    elif t.value == 'clear':
        t.type = 'CLEAR'
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