import ply.lex as lex
import ply.yacc as yacc
import sys

tokens = [
    'INT',
    'IDEN',
    'EQUALS',
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'DCL',
    'ASSIGN'
]

t_EQUALS = r'\='
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'

t_ignore = r' '

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_DCL(t):
    r'DCL'
    t.type = 'DCL'
    return t

def t_ASSIGN(t):
    r'DEFAULT'
    t.type = 'ASSIGN'
    return t

def t_IDEN(t):
    r'[a-zA-Z_][a-zA-Z_0-9@#]*'
    t.type = 'IDEN'
    return t

def t_error(t):
    print ("Illegal input!")
    t.lexer.skip(1)

lexer = lex.lex()

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE')
)

def p_parse(p):
    '''
    parse : expression
          | var_declare
          | var_assign
          | empty
    '''
    print(run(p[1]))

def p_var_declare(p):
    '''
    var_declare : DCL IDEN value
    '''
    p[0] = ('DCL', p[2], p[3])

def p_value(p):
    '''
    value : initialize
          | empty
    '''
    p[0] = p[1]

def p_initialize(p):
    '''
    initialize : ASSIGN expression
    '''
    p[0] = p[2]

def p_var_assign(p):
    '''
    var_assign : IDEN EQUALS expression
               | IDEN EQUALS IDEN
    '''
    p[0] = ('=', p[1], p[3])

def p_expression(p):
    '''
    expression : expression MULTIPLY expression
               | expression DIVIDE expression
               | expression PLUS expression
               | expression MINUS expression
    '''
    p[0] = (p[2], p[1], p[3])
    
def p_expression_int(p):
    '''
    expression : INT
    '''
    p[0] = p[1]

def p_expression_var(p):
    '''
    expression : IDEN
    '''
    p[0] = ('var', p[1])

def p_error(p):
    print("Syntax error found!")

def p_empty(p):
    '''
    empty :
    '''
    p[0] = 0

parser = yacc.yacc()

variables = {}

def run(p):
    if type(p) == tuple:
        if p[0] == '+':
            return run(p[1]) + run(p[2])
        elif p[0] == '-':
            return run(p[1]) - run(p[2])
        elif p[0] == '*':
            return run(p[1]) * run(p[2])
        elif p[0] == '/':
            return run(p[1]) / run(p[2])
        elif p[0] == '=':
            variables[p[1]] = run(p[2])
            print(variables)
        elif p[0] == 'var':
            if p[1] not in variables:
                return 'Undeclared variable Found!'
            else:
                return variables[p[1]]
        elif p[0] == 'DCL':            
            variables[p[1]] = run(p[2])
            print(p)
            print(variables)
    else:
        return p

# ortegajosant

while True:
    try:
        s = input('>>> ')
    except EOFError:
        break
    parser.parse(s)
