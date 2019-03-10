import ply.lex as lex
import ply.yacc as yacc
import sys

variables = {}

tokens = [
    'INT',
    'IDEN',
    'EQUALS',
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'DCL',
    'ASSIGN',
    'LESS',
    'MORE',
    'NON_EQUAL',
    'LESS_EQUAL',
    'MORE_EQUAL'
]

t_EQUALS = r'[\s]*\=[\s]*'
t_PLUS = r'[\s]*\+[\s]*'
t_MINUS = r'[\s]*\-[\s]*'
t_MULTIPLY = r'[\s]*\*[\s]*'
t_DIVIDE = r'[\s]*\/[\s]*'

t_LESS = r'[\s]*<[\s]*'
t_MORE = r'[\s]*>[\s]*'
t_NON_EQUAL = r'[\s]*<>[\s]*'
t_LESS_EQUAL = r'[\s]*<=[\s]*'
t_MORE_EQUAL = r'[\s]*>=[\s]*'

#Tomar medidas con print's y return's

#t_ignore = r' '

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_DCL(t):
    r'[\s]*DCL[\s]+'
    t.type = 'DCL'
    return t

def t_ASSIGN(t):
    r'[\s]+DEFAULT[\s]+'
    t.type = 'ASSIGN'
    return t

def t_IDEN(t):
    r'[a-zA-Z_][a-zA-Z_0-9@#]*'
    t.type = 'IDEN'
    return t

def t_error(t):
    if ("DEFAULT" in t.value):
        print ("Wrong declaration of variable!")
    elif (" " == t.value[0]):
        print ("You should use 'DEFAULT' to assign a value!")
    else:
        print ("Illegal input!")
    t.lexer.skip(1)

lexer = lex.lex()

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE')
)

def p_parse(p):
    '''
    parse : comparative
          | expression
          | var_declare
          | var_assign
          | empty
    '''
    #print(p[1])
    run(p[1])

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

def p_comparative(p):
    '''
    comparative : expression EQUALS EQUALS expression
                | IDEN EQUALS EQUALS expression
    '''
    comp1 = p[1]
    if type(p[1]) == str:
        comp1 = ('var', p[1])
    p[0] = ('==', comp1, p[4])

def p_var_assign(p):
    '''
    var_assign : IDEN EQUALS expression
    '''
    p[0] = ('=', p[1], p[3])

def p_expression(p):
    '''
    expression : expression MULTIPLY expression
               | expression DIVIDE expression
               | expression PLUS expression
               | expression MINUS expression
               | expression condition expression
    '''
    p[0] = (p[2], p[1], p[3])
    
def p_expression_var(p):
    '''
    expression : IDEN
    '''
    p[0] = ('var', p[1])

def p_expression_int(p):
    '''
    expression : INT
    '''
    p[0] = p[1]

def p_condition(p):
    '''
    condition : LESS
              | MORE
              | NON_EQUAL
              | LESS_EQUAL
              | MORE_EQUAL
    '''

    p[0] = p[1].strip()

def p_error(p):
    print("Syntax error found!")

def p_empty(p):
    '''
    empty :
    '''
    p[0] = 0

parser = yacc.yacc()

def run(p):
    if type(p) == tuple:

        #   SUMA
        if p[0] == '+':
            try:
                return run(p[1]) + run(p[2])
            except TypeError:
                return "Undefined Variable Found!"

        #   RESTA
        elif p[0] == '-':
            try:
                return run(p[1]) - run(p[2])
            except TypeError:
                return "Undefined Variable Found!"

        #   MULTIPLICACION
        elif p[0] == '*':
            try:
                return run(p[1]) * run(p[2])
            except TypeError:
                return "Undefined Variable Found!"

        #   DIVISION
        elif p[0] == '/':
            try:
                return int (run(p[1]) / run(p[2]))
            except TypeError:
                return "Undefined Variable Found!"
        
        #   ASIGNACION    
        elif p[0] == '=':
            if p[1] not in variables:
                return "Undeclared variable Found!"
            else:
                x = run(p[2])
                try:
                    variables[p[1]] = 0 + x
                    print(variables)
                except TypeError:
                    return x

        #   VARIABLE
        elif p[0] == 'var':
            if p[1] not in variables:
                return "Undeclared variable Found!"
            else:
                return variables[p[1]]

        #   DECLARACION
        elif p[0] == 'DCL':
            if p[1] in variables:
                return "You've already declared this variable!"
            else:
                variables[p[1]] = run(p[2])
                print(variables)

        #   'IGUAL QUE'                
        elif p[0] == '==':
            first_compared = run(p[1])
            second_compared = run(p[2])
            if type(first_compared) == int and type(second_compared) == int:
                return first_compared == second_compared
            elif type(first_compared) == str and type(second_compared) == str:
                return "Both variables are undeclared!"
            else:
                return "One variable is undeclared!"

        #   'MENOR QUE'
        elif p[0] == '<':
            first_compared = run(p[1])
            second_compared = run(p[2])
            if type(first_compared) == int and type(second_compared) == int:
                return first_compared < second_compared
            elif type(first_compared) == str and type(second_compared) == str:
                return "Both variables are undeclared!"
            else:
                return "One variable is undeclared!"

        #   'MAYOR QUE'
        elif p[0] == '>':
            first_compared = run(p[1])
            second_compared = run(p[2])
            if type(first_compared) == int and type(second_compared) == int:
                return first_compared > second_compared
            elif type(first_compared) == str and type(second_compared) == str:
                return "Both variables are undeclared!"
            else:
                return "One variable is undeclared!"

        #   'DIFERENTE QUE'
        elif p[0] == '<>':
            first_compared = run(p[1])
            second_compared = run(p[2])
            if type(first_compared) == int and type(second_compared) == int:
                return first_compared != second_compared
            elif type(first_compared) == str and type(second_compared) == str:
                return "Both variables are undeclared!"
            else:
                return "One variable is undeclared!"

        #   'MENOR O IGUAL QUE'
        elif p[0] == '<=':
            first_compared = run(p[1])
            second_compared = run(p[2])
            if type(first_compared) == int and type(second_compared) == int:
                return first_compared <= second_compared
            elif type(first_compared) == str and type(second_compared) == str:
                return "Both variables are undeclared!"
            else:
                return "One variable is undeclared!"

        #   'MAYOR O IGUAL QUE'
        elif p[0] == '>=':
            first_compared = run(p[1])
            second_compared = run(p[2])
            if type(first_compared) == int and type(second_compared) == int:
                return first_compared >= second_compared
            elif type(first_compared) == str and type(second_compared) == str:
                return "Both variables are undeclared!"
            else:
                return "One variable is undeclared!"
    else:
        return p

'''
while True:
    try:
        s = input('>>> ')
    except EOFError:
        break
    parser.parse(s)
'''

s = 'DCL a;a=3+57*788+79-90*2;a=10+r'uty'

def Parse_Code(code):
    code = s.strip().replace('\n','').split(';')
    for i in code:
        i = i.strip()
        parser.parse(i)

Parse_Code(s)
