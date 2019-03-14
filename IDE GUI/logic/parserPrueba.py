import lib.ply.lex as lex
import lib.ply.yacc as yacc
import random

variables = {}

st = ''

error = False

line = 0

valid_movements = {'AF': 1, 'F': 2, 'DFA': 3, 'IFA': 4,
                   'DFB': 5, 'IFB': 6, 'A': 7, 'DAA': 8,
                   'IAA': 9, 'DAB': 10, 'IAB': 11, 'AA': 12}

tokens = ['INT','IDEN','EQUALS','PLUS','MINUS','MULTIPLY','DIVIDE','DCL','ASSIGN','SAME','LESS','MORE','NON_EQUAL','LESS_EQUAL','MORE_EQUAL','ENCASO',
          'CUANDO','ENTONS','SINO','FINCASO','SEPARATOR','LBRACE','RBRACE','REPITA','MIENTRAS','FINDESDE','DESDE','HASTA','HAGA','INC','DEC','INI','COMMA','LPAR','RPAR',
          'MOVER','ALEATORIO']

#reserved_words = ['DCL','DEFAULT','ENCASO','FINCASO','SINO','ENTONS','CUANDO','REPITA','HASTAENCONTRAR']

t_SAME = r'[\s]*\=\=[\s]*'
t_LESS = r'[\s]*\<[\s]*'
t_MORE = r'[\s]*\>[\s]*'
t_NON_EQUAL = r'[\s]*\<\>[\s]*'
t_LESS_EQUAL = r'[\s]*\<\=[\s]*'
t_MORE_EQUAL = r'[\s]*\>\=[\s]*'

t_EQUALS = r'[\s]*\=[\s]*'
t_PLUS = r'[\s]*\+[\s]*'
t_MINUS = r'[\s]*\-[\s]*'
t_MULTIPLY = r'[\s]*\*[\s]*'
t_DIVIDE = r'[\s]*\/[\s]*'

t_SEPARATOR = r'[\s]*\;[\s]*'
t_LBRACE = r'[\s]*\{[\s]*'
t_RBRACE = r'[\s]*\}[\s]*'

t_COMMA = r'[\s]*\,[\s]*'
t_LPAR = r'[\s]*\([\s]*'
t_RPAR = r'[\s]*\)[\s]*'

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

def t_ENCASO(t):
    r'[\s]*ENCASO[\s]+'
    t.type = 'ENCASO'
    return t

def t_CUANDO(t):
    r'[\s]*CUANDO[\s]+'
    t.type = 'CUANDO'
    return t

def t_ENTONS(t):
    r'[\s]+ENTONS[\s]*'
    t.type = 'ENTONS'
    return t

def t_SINO(t):
    r'[\s]*SINO[\s]*'
    t.type = 'SINO'
    return t

def t_FINCASO(t):
    r'[\s]*FINCASO[\s]*'
    t.type = 'FINCASO'
    return t

def t_REPITA(t):
    r'[\s]*REPITA[\s]+'
    t.type = 'REPITA'
    return t

def t_MIENTRAS(t):
    r'[\s]+MIENTRAS[\s]+'
    t.type = 'MIENTRAS'
    return t

def t_FINDESDE(t):
    r'[\s]*FINDESDE[\s]*'
    t.type = 'FINDESDE'
    return t

def t_DESDE(t):
    r'[\s]*DESDE[\s]*'
    t.type = 'DESDE'
    return t

def t_HASTA(t):
    r'[\s]*HASTA[\s]*'
    t.type = 'HASTA'
    return t

def t_HAGA(t):
    r'[\s]*HAGA[\s]*'
    t.type = 'HAGA'
    return t

def t_INC(t):
    r'[\s]*Inc'
    t.type = 'INC'
    return t

def t_DEC(t):
    r'[\s]*Dec'
    t.type = 'DEC'
    return t

def t_INI(t):
    r'[\s]*Ini'
    t.type = 'INI'
    return t


def t_MOVER(t):
    r'[\s]*Mover'
    t.type = 'MOVER'
    return t

def t_ALEATORIO(t):
    r'[\s]*Aleatorio'
    t.type = 'ALEATORIO'
    return t

def t_IDEN(t):
    r'[a-zA-Z_][a-zA-Z_0-9@#]*'
    '''global reserved_words
    if t.value in reserved_words:
        if reserved_words.index(t.value) == 'DEFAULT':
            t.type = reserved_words(reserved_words.index(t.value))
        else:
            t.type = t.value

    else:'''
    t.type = 'IDEN'
    return t

def t_error(t):
    global error
    global st
    error = True
    if ("DEFAULT" in t.value):
        st += "Wrong declaration of variable!"
    else:
        st += " because there's a illegal input"
    while t.lexer.lexpos < t.lexer.lexlen:
        t.lexer.skip(1)
    t.lexer.skip(1)


lexer = lex.lex()

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE')
)

def p_parse(p):
    '''
    parse : comparative
          | sentence
          | cases
          | empty
          | repeat
          | do
          | function
    '''
    print(p[1])
    run(p[1])

def p_function(p):
    '''
    function : moves
             | random
             | changes
    '''
    p[0] = ('function',) + p[1]

def p_changes(p):
    '''
    changes : MOVER LPAR IDEN RPAR
    '''
    p[0] = (p[1].strip(),p[3])

def p_random(p):
    '''
    random : ALEATORIO LPAR RPAR
    '''
    p[0] = (p[1].strip(),)

def p_moves(p):
    '''
    moves : moves_aux LPAR IDEN COMMA INT RPAR
    '''
    p[0] = (p[1],p[3],p[5])

def p_moves_aux(p):
    '''
    moves_aux : INC
              | DEC
              | INI
    '''
    p[0] = p[1].strip()

def p_do(p):
    '''
    do : DESDE IDEN EQUALS expression HASTA expression HAGA actions FINDESDE
    '''
    p[0] = ('haga',p[2],p[4],p[6],p[8])

def p_repeat(p):
    '''
    repeat : REPITA actions MIENTRAS comparative
    '''
    p[0] = ('repetir',p[2],p[4])

def p_cases(p):
    '''
    cases : syntax1
          | syntax2
    '''
    p[0] = p[1]

def p_syntax2(p):
    '''
    syntax2 : ENCASO IDEN options2 SINO LBRACE actions RBRACE FINCASO
    '''
    p[0] = ('caso',('var',p[2]),p[3],p[6])

def p_options2(p):
    '''
    options2 : CUANDO condition expression ENTONS LBRACE actions RBRACE more_options2
    '''
    p[0] = () + ((p[2].strip(),p[3],p[6]),) + p[8]

def p_more_options2(p):
    '''
    more_options2 : options2
                 | empty
    '''
    p[0] = p[1]
    if p[0] == 0:
        p[0] = ()

def p_syntax1(p):
    '''
    syntax1 : ENCASO options1 SINO LBRACE actions RBRACE FINCASO
    '''
    p[0] = ('caso',p[2],p[5])

def p_options1(p):
    '''
    options1 : CUANDO comparative ENTONS LBRACE actions RBRACE more_options1
    '''
    p[0] = () + ((p[2],p[5]),) + p[7]

def p_more_options1(p):
    '''
    more_options1 : options1
                 | empty
    '''
    p[0] = p[1]
    if p[0] == 0:
        p[0] = ()

def p_actions(p):
    '''
    actions : var_assign more_actions
    '''
    p[0] = (p[1],) + p[2]

def p_more_actions(p):
    '''
    more_actions : SEPARATOR more_actions_aux
                 | empty
    '''
    if p[1] == 0:
        p[0] = ()
    else:
        if p[2] == 0:
            p[0] = ()
        else:
            p[0] = p[2]

def p_more_actions_aux(p):
    '''
    more_actions_aux : actions
                     | empty
    '''
    p[0] = p[1]

def p_sentence(p):
    '''
    sentence : var_declare
             | var_assign
    '''
    p[0] = p[1]

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
    comparative : IDEN condition expression
    '''
    p[0] = (p[2].strip(), ('var',p[1]), p[3])


def p_var_assign(p):
    '''
    var_assign : IDEN EQUALS expression
    '''
    p[0] = (p[2].strip(), ('var',p[1]), p[3])

def p_expression(p):
    '''
    expression : expression operator expression
    '''
    p[0] = (p[2].strip(), p[1], p[3])


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

def p_operator(p):
    '''
    operator : MULTIPLY
             | DIVIDE
             | PLUS
             | MINUS
    '''
    p[0] = p[1]

def p_condition(p):
    '''
    condition : SAME
              | LESS
              | MORE
              | NON_EQUAL
              | LESS_EQUAL
              | MORE_EQUAL
    '''

    p[0] = p[1]

def p_error(p):
    global st
    global error
    global line
    error = True
    if not ("--> A syntax error was found" in st):
        st = "--> A syntax error was found in line " + str(line) + "!"

def p_empty(p):
    '''
    empty :
    '''
    p[0] = 0


parser = yacc.yacc()


def run(p):
    global st
    global error
    if type(p) == tuple:

        #   SUMA
        if p[0] == '+':
            try:
                return run(p[1]) + run(p[2])
            except TypeError:
                error = True
                return "Undefined Variable Found!"

        #   RESTA
        elif p[0] == '-':
            try:
                return run(p[1]) - run(p[2])
            except TypeError:
                error = True
                return "Undefined Variable Found!"

        #   MULTIPLICACION
        elif p[0] == '*':
            try:
                return run(p[1]) * run(p[2])
            except TypeError:
                error = True
                return "Undefined Variable Found!"

        #   DIVISION
        elif p[0] == '/':
            try:
                return int(run(p[1]) / run(p[2]))
            except TypeError:
                error = True
                return "Undefined Variable Found!"

        #   ASIGNACION
        elif p[0] == '=':
            if p[1][1] not in variables:
                error = True
                st += "--> You tried to assign a value to an undeclared variable!"
            else:
                x = run(p[2])
                try:
                    variables[p[1][1]] = 0 + x
                    st += '--> ' + p[1][1] + ' = ' + str(x)
                except TypeError:
                    error = True
                    st += x

        #   VARIABLE
        elif p[0] == 'var':
            if p[1] not in variables:
                error = True
                return "--> Undeclared variable found!"
            else:
                return variables[p[1]]

        #   DECLARACION
        elif p[0] == 'DCL':
            if p[1] in variables:
                error = True
                st += "--> You've already declared the variable " + p[1] + " !"
            else:
                assignment = run(p[2])
                if type(assignment) == str:
                    error = True
                    st += "--> You put a non-valid default value" + "!"
                else:
                    variables[p[1]] = assignment
                    st += '--> New variable: ' + p[1] + ' = ' + str(run(p[2]))

        #   'IGUAL QUE'
        elif p[0] == '==':
            first_compared = run(p[1])
            second_compared = run(p[2])
            if type(first_compared) == int and type(second_compared) == int:
                return first_compared == second_compared
            elif type(first_compared) == str and type(second_compared) == str:
                return "Both expressions are undeclared!"
            else:
                return "One expression is undeclared!"

        #   'MENOR QUE'
        elif p[0] == '<':
            first_compared = run(p[1])
            second_compared = run(p[2])
            if type(first_compared) == int and type(second_compared) == int:
                return first_compared < second_compared
            elif type(first_compared) == str and type(second_compared) == str:
                return "Both expressions are undeclared!"
            else:
                return "One expression is undeclared!"

        #   'MAYOR QUE'
        elif p[0] == '>':
            first_compared = run(p[1])
            second_compared = run(p[2])
            if type(first_compared) == int and type(second_compared) == int:
                return first_compared > second_compared
            elif type(first_compared) == str and type(second_compared) == str:
                return "Both expressions are undeclared!"
            else:
                return "One expression is undeclared!"

        #   'DIFERENTE QUE'
        elif p[0] == '<>':
            first_compared = run(p[1])
            second_compared = run(p[2])
            if type(first_compared) == int and type(second_compared) == int:
                return first_compared != second_compared
            elif type(first_compared) == str and type(second_compared) == str:
                return "Both expressions are undeclared!"
            else:
                return "One expression is undeclared!"

        #   'MENOR O IGUAL QUE'
        elif p[0] == '<=':
            first_compared = run(p[1])
            second_compared = run(p[2])
            if type(first_compared) == int and type(second_compared) == int:
                return first_compared <= second_compared
            elif type(first_compared) == str and type(second_compared) == str:
                return "Both expressions are undeclared!"
            else:
                return "One expression is undeclared!"

        #   'MAYOR O IGUAL QUE'
        elif p[0] == '>=':
            first_compared = run(p[1])
            second_compared = run(p[2])
            if type(first_compared) == int and type(second_compared) == int:
                return first_compared >= second_compared
            elif type(first_compared) == str and type(second_compared) == str:
                return "Both expressions are undeclared!"
            else:
                return "One expression is undeclared!"

        elif p[0] == 'caso':
            if len(p) == 3:
                st += "--> Syntax 1 "
                exit = False
                case = 1
                for i in p[1]:
                    x = run(i[0])
                    if type(x) == str:
                        st += x
                        return
                    elif x == True:
                        exit = True
                        for j in i[1]:
                            run(j)
                        st += " --> Acciones del Caso " + str(case) + " bien hechas!"
                    case += 1
                if exit == False:
                    for k in p[2]:
                        run(k)
                    st += " --> Acciones del SINO bien hechas!"
            else:
                st += "--> Syntax 2"
                exit = False
                case = 1
                for i in p[2]:
                    y = (i[0],p[1],i[1])
                    x = run(y)
                    print(y)
                    print(x)
                    if type(x) == str:
                        st += x
                        return
                    elif x == True:
                        exit = True
                        for j in i[2]:
                            run(j)
                        break
                    case += 1
                if exit == True:
                    st += " --> Acciones del Caso " + str(case) + " bien hechas!"
                else:
                    for k in p[3]:
                        run(k)
                    st += " --> Acciones del SINO bien hechas!"


        elif p[0] == 'repetir':
            st += "--> Repeticion"
            while True:
                for i in p[1]:
                    st += " "
                    run(i)
                if (run(p[2]) == False):
                    break;
            st += " --> Repeticion finalizada!"

        elif p[0] == 'haga':
            if p[1] not in variables:
                st += "--> The variable " + p[1] + " hasn't been declared!"
                error = True
                return
            else:
                st += "--> Haga esto! "
                minor = p[2]
                major = p[3]
                if minor > major:
                    temp = major
                    major = minor
                    minor = temp
                if minor == major:
                    return
                variables[p[1]] = minor
                while variables[p[1]] <= major:
                    for i in p[4]:
                        run(i)
                        st += " "
                    variables[p[1]] += 1
                st += " --> Terminado"


        elif p[0] == 'function':
            if p[1] == 'Aleatorio':
                i = 1
                while i < 11:
                    move = random.choice(list(valid_movements.items()))
                    st += "--> Movimiento aleatorio " + str(i) + ": Mover hacia " + move[0] + " = " + str(move[1]) + "!\n"
                    i += 1
            elif p[1] == 'Mover':
                if p[2] in valid_movements:
                    st += "--> Mover hacia " + p[2] + " = " + str(valid_movements[p[2]]) + "!"
                else:
                    error = True
                    st += "--> Movimiento " + p[2] + " no válido!"
            else:
                if p[2] in variables:
                    if p[1] == 'Inc':
                        variables[p[2]] += p[3]
                        st += "--> Valor de " + p[2] + " incrementado en " + str(p[3]) + "!"
                    elif p[1] == 'Dec':
                        variables[p[2]] -= p[3]
                        st += "--> Valor de " + p[2] + " decrementado en " + str(p[3]) + "!"
                    else:
                        variables[p[2]] = p[3]
                        st += "--> Valor de " + p[2] + " cambiado por " + str(p[3]) + "!"
                else:
                    error = True
                    st += "--> " + p[2] + " no ha sido declarado!"

    else:
        return p

def Parse_Code(code):
    code = code.strip()
    parser.parse(code)
    global st
    global error
    global line
    final_st = st
    st = ''
    error_Found = error
    error = False
    line += 1
    return final_st, error_Found
