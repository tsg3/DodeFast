import lib.ply.lex as lex
import lib.ply.yacc as yacc
import random
import time
import logic.bluetooth

buffer = []
prevCode = ""
codigo = []
procedimientos = {}
proc_called = False
proc_declarations_called = False
lineError = ""
gvariables = {}
lvariables = {}

flag_runnig = False

flag_stop = False

st = ''

error = False

line = 0

valid_movements = {'AF': '001011', 'F': '110121', 'DFA': '011120', 'IFA': '000010',
                   'DFB': '011021', 'IFB': '111111', 'A': '111020', 'DAA': '201020',
                   'IAA': '202120', 'DAB': '200020', 'IAB': '101010', 'AA': '010101'}

''' ------------------------------ ANALISIS LEXICO ------------------------------ '''

tokens = ['INT', 'IDEN', 'EQUALS', 'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'DCL', 'ASSIGN', 'SAME', 'LESS', 'MORE',
          'NON_EQUAL', 'LESS_EQUAL', 'MORE_EQUAL', 'ENCASO',
          'CUANDO', 'ENTONS', 'SINO', 'FINCASO', 'SEPARATOR', 'LBRACE', 'RBRACE', 'REPITA', 'MIENTRAS', 'FINDESDE',
          'DESDE', 'HASTA', 'HAGA', 'INC', 'DEC', 'INI', 'COMMA', 'LPAR', 'RPAR',
          'MOVER', 'ALEATORIO', 'LLAMAR']

color_words = ['DCL', 'ENCASO', 'FINCASO', 'REPITA', 'MIENTRAS', 'FINDESDE', 'DESDE', 'DEFAULT', 'CUANDO', 'ENTONS',
               'SINO', 'HASTA', 'HAGA', 'Inc', 'Dec', 'Ini', 'Mover', 'Aleatorio', 'LLAMAR', 'INICIO', 'FINAL', 'PROC',
               'FINPROC']

reserved_words = ['DCL', 'DEFAULT', 'ENCASO', 'FINCASO', 'SINO', 'ENTONS', 'CUANDO', 'REPITA', 'MIENTRAS', 'FINDESDE',
                  'DESDE', 'HASTA', 'HAGA', 'Ini', 'Dec', 'Inc', 'Mover', 'Aleatorio',
                  'LLAMAR', 'PROC', 'FINPROC', 'INICIO', 'FINAL']

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
    r'[\s]*\d+'
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


def t_LLAMAR(t):
    r'[\s]*LLAMAR[\s]+'
    t.type = 'LLAMAR'
    return t


def t_IDEN(t):
    r'[\s]*[a-zA-Z_][a-zA-Z_0-9@#]*'
    global reserved_words
    global error
    global st
    is_in = False
    value_found = ''
    for i in reserved_words:
        if i in t.value and i != t.value and not is_in:
            is_in = True
            value_found = i
        elif i in t.value and i != t.value and is_in:
            value_found += '.' + i
            break
    if t.value in reserved_words:
        if t.value == 'DEFAULT':
            t.type = 'ASSIGN'
        elif t.value == 'MIENTRAS':
            t.type = 'MIENTRAS'
        elif t.value == 'Inc':
            t.type = 'INC'
        elif t.value == 'Dec':
            t.type = 'DEC'
        elif t.value == 'Ini':
            t.type = 'INI'
        else:
            t.type = t.value
        return t
    elif is_in:
        error = True
        if '.' in value_found:
            values = ''
            for j in value_found.split('.'):
                values += ', ' + j
            values = values[2:]
            st = "\n--> ERROR LÉXICO ~~~ Se encontraron las palabras reservadas " + values
        else:
            st = "\n--> ERROR LÉXICO ~~~ Se encontró la palabra reservada " + value_found
        st += " en la expresion: " + t.value + " , en la linea " + str(get_line_error()) + "!"
        while t.lexer.lexpos < t.lexer.lexlen:
            t.lexer.skip(1)
        return
    else:
        t.type = 'IDEN'
        return t


def t_error(t):
    global error
    global st
    error = True
    st = "\n--> ERROR LÉXICO ~~~ Se encontraron una expresion no válida: " + t.value + " , en la linea " + str(
        get_line_error()) + "!"
    while t.lexer.lexpos < t.lexer.lexlen:
        t.lexer.skip(1)


lexer = lex.lex()

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE')
)

''' ------------------------------ ANALISIS SINTACTICO ------------------------------ '''


def p_parse(p):
    '''
    parse : comparative
          | sentence
          | var_declare
          | proc
          | IDEN
          | empty
    '''
    #print(p[1])
    global error
    global st
    if error or type(p[1]) == str:
        if type(p[1]) == str:
            st = "\n--> ERROR SINTÁCTICO en la linea " + str(
                get_line_error()) + " ~~~ '{}' no es una sentencia válida!".format(p[1])
        error = True
        return
    run(p[1])


def p_proc(p):
    '''
    proc : LLAMAR IDEN LPAR params RPAR
    '''
    p[0] = ('llamar', p[2], p[4])


def p_params(p):
    '''
    params : expression more_params
    '''
    p[0] = (p[1],) + p[2]


def p_more_params(p):
    '''
    more_params : COMMA params
                | empty
    '''
    if p[1] == 0:
        p[0] = ()
    else:
        p[0] = p[2]


def p_sentence(p):
    '''
    sentence : var_assign
             | cases
             | repeat
             | do
             | function
             | proc
    '''
    p[0] = p[1]


def p_function(p):
    '''
    function : moves
             | random
             | changes
    '''
    p[0] = ('function',) + p[1]


def p_moves(p):
    '''
    moves : MOVER LPAR IDEN RPAR
    '''
    p[0] = (p[1].strip(), p[3])


def p_random(p):
    '''
    random : ALEATORIO LPAR RPAR
    '''
    p[0] = (p[1].strip(),)


def p_changes(p):
    '''
    changes : changes_aux LPAR IDEN COMMA INT RPAR
    '''
    p[0] = (p[1], p[3], p[5])


def p_changes_aux(p):
    '''
    changes_aux : INC
                | DEC
                | INI
    '''
    p[0] = p[1].strip()


def p_do(p):
    '''
    do : DESDE IDEN EQUALS expression HASTA expression HAGA actions FINDESDE
    '''
    p[0] = ('haga', p[2], p[4], p[6], p[8])


def p_repeat(p):
    '''
    repeat : REPITA actions MIENTRAS comparative
    '''
    p[0] = ('repetir', p[2], p[4])


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
    p[0] = ('caso', ('var', p[2]), p[3], p[6])


def p_options2(p):
    '''
    options2 : CUANDO condition expression ENTONS LBRACE actions RBRACE more_options2
    '''
    p[0] = () + ((p[2].strip(), p[3], p[6]),) + p[8]


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
    p[0] = ('caso', p[2], p[5])


def p_options1(p):
    '''
    options1 : CUANDO comparative ENTONS LBRACE actions RBRACE more_options1
    '''
    p[0] = () + ((p[2], p[5]),) + p[7]


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
    actions : sentence more_actions
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
    p[0] = ("comparacion", p[2].strip(), ('var', p[1]), p[3])


def p_var_assign(p):
    '''
    var_assign : IDEN EQUALS expression
    '''
    p[0] = (p[2].strip(), ('var', p[1]), p[3])


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

    # TESTEO
    try:
        error_type = parser.symstack[1].type

        if parser.symstack[1].type == 'ENCASO' and len(parser.symstack) > 2:
            if parser.symstack[2].type == 'IDEN' or parser.symstack[2].type == 'CUANDO':
                error_type += parser.symstack[2].type

        #stack_state_str = ' '.join([symbol.type for symbol in parser.symstack][1:])

        #print('Syntax error in input! Parser State:{} {} . {}'.format(parser.state, stack_state_str, p))

        # print(error_type)
        error_message = error_cases(error_type.strip())
        if not ("sintaxis" in st) and "expresion" not in st:
            st = "\n--> ERROR SINTÁCTICO ~~~ La expresion " + str(
                p.value) + " causa un error de sintaxis en la linea " + str(get_line_error()) + ":" + error_message
            return
    except IndexError:
        if not ("sintaxis" in st) and "expresion" not in st:
            st = "\n--> ERROR SINTÁCTICO ~~~ La expresion " + str(p.value) \
                 + " en la linea " + str(
                get_line_error()) + " no se encuentra al inicio de ninguna estructura válida!\n--> " \
                                    "Estructuras válidas que incluyen " + str(p.value) + ":" + error_cases(
                p.type.strip())
    return


'''def p_error(p):

    # get formatted representation of stack
    stack_state_str = ' '.join([symbol.type for symbol in parser.symstack][1:])

    print('Syntax error in input! Parser State:{} {} . {}'.format(parser.state,stack_state_str,p))'''


def p_empty(p):
    '''
    empty :
    '''
    p[0] = 0


def error_cases(instruccion):
    if instruccion == 'ENTONS' or instruccion == 'SINO' or instruccion == 'FINCASO':
        instruccion = 'CUANDO'
    if instruccion == 'HAGA' or instruccion == 'FINDESDE':
        instruccion = 'HASTA'
    cases = {
        'DCL': "\n--> Sintaxis para una Declaración: 'DCL <variable>' o 'DCL <variable> DEFAULT <variable|número>'",
        'IDEN': "\n--> Sintaxis para una Asignación: 'IDEN = <expresión>'. <expresión> puede ser una variable, un número o operaciones entre éstos.",
        'REPITA': "\n--> Sintaxis para un Repeticiones: 'REPITA <acciones> MIENTRAS <comparativo>'.",
        'DESDE': "\n--> Sintaxis para un Desde: 'DESDE <variable> = <expresión> HASTA <expresión> HAGA <acciones> FINDESDE'.",
        'changes_aux': "\n--> Sintaxis para funciones básicas: '<Inc|Dec|Ini> ( <variable> , <número> )'.",
        'MOVER': "\n--> Sintaxis para la función Mover: 'Mover ( <variable> )'. La variable solo puede ser: AF, F, DFA, IFA, DFB, IFB, A, DAA, IAA, DAB, IAB y AA.",
        'ALEATORIO': "\n--> Sintaxis para la función Aleatorio: 'Aleatorio ( )'.",
        'LLAMAR': "\n--> Sintaxis para la llamar procedimientos: 'LLAMAR <procedimiento> ( <parametros>* )'.",
        'ENCASO': "\n--> Sintaxis para Casos:"
                  "\n--> Sintaxis 1 para Casos: 'ENCASO <casos1> SINO { <acciones> } FINCASO'. Los <casos1> son: 'CUANDO <comparativo> ENTONS { <acciones> }'."
                  "\n--> Sintaxis 2 para Casos: 'ENCASO <variable> <casos2> SINO { <acciones> } FINCASO'. Los <casos2> son: 'CUANDO <condición> <expresión> ENTONS { <acciones> }'.",
        'ENCASOCUANDO': "\n--> Sintaxis 1 para Casos: 'ENCASO <casos1> SINO { <acciones> } FINCASO'. Los <casos1> son: 'CUANDO <comparativo> ENTONS { <acciones> }'.",
        'ENCASOIDEN': "\n--> Sintaxis 2 para Casos: 'ENCASO <variable> <casos2> SINO { <acciones> } FINCASO'. Los <casos2> son: 'CUANDO <condición> <expresión> ENTONS { <acciones> }'.",

        'ASSIGN': "\n--> Declaraciones: 'DCL <variable> DEFAULT <variable|número>'.",
        'CUANDO': "\n--> Casos:"
                  "\n--> Sintaxis 1 para Casos: 'ENCASO <casos1> SINO { <acciones> } FINCASO'. Los <casos1> son: 'CUANDO <comparativo> ENTONS { <acciones> }'."
                  "\n--> Sintaxis 2 para Casos: 'ENCASO <variable> <casos2> SINO { <acciones> } FINCASO'. Los <casos2> son: 'CUANDO <condición> <expresión> ENTONS { <acciones> }'.",
        'MIENTRAS': "\n--> Repeticiones: 'REPITA <acciones> MIENTRAS <comparativo>'.",
        'HASTA': "\n--> Desde: 'DESDE <variable> = <expresión> HASTA <expresión> HAGA <acciones> FINDESDE'."

    }
    func = cases.get(instruccion, "\n--> Nada")
    return func


parser = yacc.yacc()

''' ------------------------------ ANALISIS SEMANTICO ------------------------------ '''


def run(p):
    global st
    global error
    global proc_called
    global gvariables
    global lvariables
    global proc_declarations_called
    global lineError

    if proc_called == True:
        variables = lvariables
    else:
        variables = gvariables

    if type(p) == tuple:

        if p[0] != 'DCL' and p[0] != 'var' and proc_declarations_called == True:
            error = True
            st = "\n--> ERROR SEMANTICO ~~~ Sentencia ejecutada en la linea " + str(get_line_error()) + \
                 "!\n--> No se puede ejecutar sentencias que no sean declaraciones en esa sección de un procedimiento."
            return

        #   SUMA
        elif p[0] == '+':
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
                st = "\n--> ERROR SEMANTICO ~~~ Sentencia ejecutada en la linea " + str(get_line_error()) + \
                     "!\n--> Se esta asignando un valor a la variable " + p[1][1] + " cuando esta no ha sido declarada."
            else:
                x = run(p[2])
                try:
                    variables[p[1][1]] = 0 + x
                    st += '\n--> ' + p[1][1] + ' = ' + str(x)
                except TypeError:
                    error = True

        #   VARIABLE
        elif p[0] == 'var':
            if p[1].strip() not in variables:
                error = True
                st = "\n--> ERROR SEMANTICO ~~~ Sentencia ejecutada en la linea " + str(get_line_error()) + \
                     "!\n--> La variable " + p[1] + " no ha sido declarada."
                print(variables)
                print(p[1])
                return ""
            else:
                return variables[p[1].strip()]

        #   DECLARACION
        elif p[0] == 'DCL':
            if proc_called == True and proc_declarations_called == False:
                error = True
                st = "\n--> ERROR SEMANTICO ~~~ Sentencia ejecutada en la linea " + str(get_line_error()) + \
                     "!\n--> No se puede declarar variables en la ejecucion de un procedimiento."
            else:
                if p[1] in variables:
                    error = True
                    st = "\n--> ERROR SEMANTICO ~~~ Sentencia ejecutada en la linea " + str(get_line_error()) + \
                         "!\n--> La variable " + p[1] + " ya ha sido declarada."
                else:
                    assignment = run(p[2])
                    if type(assignment) == bool and not assignment:
                        error = True
                    else:
                        variables[p[1]] = assignment
                        st += '\n--> Nueva variable: ' + p[1] + ' = ' + str(run(p[2]))

        #   Comparaciones
        elif p[0] == 'comparacion':
            first_compared = run(p[2])
            second_compared = run(p[3])
            if type(first_compared) == int and type(second_compared) == int:
                if p[1] == '==':
                    return first_compared == second_compared
                elif p[1] == '<':
                    return first_compared < second_compared
                elif p[1] == '>':
                    return first_compared > second_compared
                elif p[1] == '<=':
                    return first_compared <= second_compared
                elif p[1] == '>=':
                    return first_compared >= second_compared
                else:
                    return first_compared != second_compared
            elif type(first_compared) == str and type(second_compared) == str:
                return "error"

            else:
                return "error"

        #   'CASOS'
        elif p[0] == 'caso':
            if len(p) == 3:
                exit = False
                case = 1
                for i in p[1]:
                    x = run(i[0])
                    if type(x) == str:
                        return
                    elif x == True:
                        exit = True
                        for j in i[1]:
                            run(j)
                            if error:
                                break
                        if not error:
                            st += " \n--> Acciones del Caso " + str(case) + " bien hechas!"
                    case += 1
                if exit == False and not error:
                    for k in p[2]:
                        run(k)
                        if error:
                            break
                    if not error:
                        st += " \n--> Acciones del SINO bien hechas!"
            else:
                exit = False
                case = 1
                for i in p[2]:
                    y = ('comparacion', i[0], p[1], i[1])
                    x = run(y)
                    if type(x) == str:
                        return
                    elif x == True:
                        exit = True
                        for j in i[2]:
                            run(j)
                            if error:
                                break
                        break
                    case += 1
                if exit == True and not error:
                    st += "\n--> Acciones del Caso " + str(case) + " bien hechas!"
                else:
                    for k in p[3]:
                        run(k)
                        if error:
                            break
                    if not error:
                        st += "\n--> Acciones del SINO bien hechas!"

        #   'HACER'
        elif p[0] == 'repetir':
            global flag_stop
            while True:
                for i in p[1]:
                    st += " "
                    run(i)
                    if error:
                        break
                    time.sleep(0.00001)
                    st = ""
                if error:
                    break
                if (run(p[2]) == False):
                    break
                if flag_stop == True:
                    flag_stop = False
                    error = True
                    st = "\n--> La ejecución fue detenida forzosamente!☻"
                    time.sleep(0.01)
                    break
                time.sleep(0.01)

        #   'HAGA'
        elif p[0] == 'haga':
            if p[1] not in variables:
                st = "\n--> ERROR SEMANTICO ~~~ Sentencia ejecutada en la linea " + str(get_line_error()) + \
                     "!\n--> La variable " + p[1] + " no ha sido declarada."
                error = True
                return
            else:
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
                        if error:
                            break
                        st += " "
                    if error:
                        break
                    variables[p[1]] += 1

        #   'FUNCIONES'
        elif p[0] == 'function':
            if p[1] == 'Aleatorio':
                i = 1
                while i < 11:
                    move = random.choice(list(valid_movements.items()))
                    st += "\n--> Movimiento aleatorio: Mover hacia " + move[0] + " = " + move[1] + "!\n"
                    i += 1
                    buffer.append(move[1])
            elif p[1] == 'Mover':
                if p[2] in valid_movements:
                    st += "\n--> Mover hacia " + p[2] + " = " + valid_movements[p[2]] + "!"
                    buffer.append(valid_movements[p[2]])
                else:
                    error = True
                    st = "\n--> ERROR SEMANTICO ~~~ Sentencia ejecutada en la linea " + str(get_line_error()) + \
                         "!\n--> El movimiento " + p[
                             2] + " no es un movimiento valido.\n--> Movimientos validos: AF, F, DFA, IFA, DFB, IFB, A, DAA, IAA, DAB, IAB y AA."
            else:
                if p[2] in variables:
                    if p[1] == 'Inc':
                        variables[p[2]] += p[3]
                        st += "\n--> Valor de " + p[2] + " incrementado en " + str(p[3]) + "!"
                    elif p[1] == 'Dec':
                        variables[p[2]] -= p[3]
                        st += "\n--> Valor de " + p[2] + " decrementado en " + str(p[3]) + "!"
                    else:
                        variables[p[2]] = p[3]
                        st += "\n--> Valor de " + p[2] + " cambiado por " + str(p[3]) + "!"
                else:
                    error = True
                    st = "\n--> ERROR SEMANTICO ~~~ Sentencia ejecutada en la linea " + str(get_line_error()) + \
                         "!\n--> La variable " + p[2] + " no ha sido declarada."

        #   'LLAMAR'
        elif p[0] == "llamar":
            if p[1] not in procedimientos:
                error = True
                st = "\n--> ERROR SEMANTICO ~~~ Sentencia ejecutada en la linea " + str(get_line_error()) + \
                     "!\n--> El procedimiento " + p[1] + " no ha sido definido."
            else:
                n = len(p[2])
                if len(p[2]) != len(procedimientos[p[1]][0]):
                    error = True
                    st = "\n--> ERROR SEMANTICO ~~~ Sentencia ejecutada en la linea " + str(get_line_error()) + \
                         "!\n--> No se ingreso la cantidad correcta de parametros para ejecutar este procedimiento."

                else:
                    proc_called = True
                    i = 0
                    while i < n:
                        value = p[2][i]
                        if type(p[2][i]) == tuple:
                            value = gvariables[p[2][i][1]]
                        lvariables[procedimientos[p[1]][0][i]] = value
                        i += 1
                    proc_declarations_called = True
                    for i in procedimientos[p[1]][2]:
                        lineError = i
                        parser.parse(i.replace("\n", " ").strip())
                        if error:
                            break
                    proc_declarations_called = False
                    for i in procedimientos[p[1]][1]:
                        lineError = i
                        parser.parse(i.replace("\n", " ").strip())
                        if error:
                            break
                    proc_called = False
                    lvariables.clear()
                    if not error:
                        st += "\n--> Ejecucion de procedimiento finalizada"
                    time.sleep(0.0005)
    else:
        return p


''' ------------------------------ PARSEO ------------------------------ '''


def parse_code(code):
    global st
    global error
    global line
    code = code.strip()
    parser.parse(code)
    final_st = st
    st = ''
    error_Found = error
    error = False
    line += 1
    return final_st, error_Found


''' ------------------------------ PARSEO DE ESTRUCTURAS EXTERNAS ------------------------------ '''


def separate_code(code):
    global st
    openbrace = 0
    pos = []

    repita = []
    mientras = []
    i = 0
    n = len(code)
    while i < n:
        digit = code.find('REPITA', i)
        if not (digit in repita) and digit != -1:
            repita.append(digit)
        digit = code.find('MIENTRAS', i)
        if not (digit in mientras) and digit != -1:
            mientras.append(digit)
        i += 1
    n = len(repita)
    if len(mientras) < n:
        n = len(mientras)
    w = 0
    inside_while = False

    haga = []
    findesde = []
    y = 0
    u = len(code)
    while y < u:
        digit = code.find('HAGA', y)
        if not (digit in haga) and digit != -1:
            haga.append(digit)
        digit = code.find('FINDESDE', y)
        if not (digit in findesde) and digit != -1:
            findesde.append(digit)
        y += 1
    p = len(haga)
    if len(findesde) < p:
        p = len(findesde)
    l = 0
    inside_do = False
    x = 0
    for i in code:
        if w < n:
            if x > repita[w]:
                inside_while = True
            if x > mientras[w]:
                inside_while = False
                w += 1
        if l < p:
            if x > haga[l]:
                inside_do = True
            if x > findesde[l]:
                inside_do = False
                l += 1
        if i == '{':
            openbrace += 1
        elif i == '}':
            openbrace -= 1
        elif i == ';' and openbrace == 0 and inside_while == False and inside_do == False:
            pos.append(x)
        x += 1
    lista = []
    n = len(pos)
    y = 0
    if len(pos) == 0:
        return code
    else:
        while y < n:
            if y == 0:
                lista.append(code[:pos[y]])
            else:
                lista.append(code[pos[y - 1] + 1:pos[y]])
            y += 1
        lista.append(code[pos[-1] + 1:])
        return lista


def get_proc(code):
    global st
    global lineError
    global procedimientos
    if len(code) == 0:
        return {}
    else:
        if code.count("PROC") == 0:
            return {}
        elif code.count("PROC") != 2 * code.count("FINPROC"):
            st = "\n--> Ejecucion finalizada debido a:\n--> ERROR SINTÁCTICO ~~~ " \
                 "Toda sentencia PROC debe ser encapsulado entre PROC - FINPROC☻"
            time.sleep(0.0005)
            return "error"
        else:
            procs = {}
            while len(code.replace("\n", " ").strip()) != 0:
                count1 = code.find("PROC")
                count3 = code.find("FINPROC")
                if count1 == -1 or count3 == -1:
                    return {}
                else:
                    proc = code[count1:count3 + 7]
                    count1 = proc.find("(")
                    count2 = proc.find(")")
                    if count1 != -1 and count2 != -1:
                        proc_name = proc[4:count1].strip().replace("\n", " ")
                        if len(proc_name) != 0:
                            count4 = count2
                            params = proc[count1 + 1:count2].split(",")
                            strip = 0
                            while strip < len(params):
                                params[strip] = params[strip].replace("\n", " ").strip()
                                strip += 1
                            repetidos = False
                            counter1 = 0
                            while counter1 < len(params):
                                counter2 = counter1 + 1
                                while 0 < len(params[counter2:]):
                                    if params[counter1] == params[counter2:][0]:
                                        repetidos = True
                                        break
                                    counter2 += 1
                                counter1 += 1
                            if repetidos == True:
                                st = "\n--> Ejecucion finalizada debido a:\n--> ERROR SINTÁCTICO ~~~ " \
                                     "Parámetros repetidos en PROC " + proc_name + "☻"
                                time.sleep(0.0005)
                                return "error"

                            count1 = proc.find("INICIO")
                            count2 = proc.find("FINAL")
                            if count1 != -1 and count2 != -1:
                                declarations = proc[count4 + 1:count1].split(";")
                                #print("DEC", declarations)
                                #print(declarations,verificar_ultimo(declarations[-1]))
                                if not verificar_ultimo(declarations[-1]):
                                    lineError = declarations[-1]
                                    procs[proc_name] = (tuple(params), [], list(filter(None, declarations)))
                                    procedimientos = procs
                                    #print(procedimientos)
                                    st = "\n--> Ejecucion finalizada debido a:\n--> ERROR SINTÁCTICO ~~~ " \
                                         "Ausencia de ';' en la linea " + str(get_line_error()) + "!☻"
                                    time.sleep(0.0005)
                                    return "error"
                                proc_code = get_code(proc[count1:], True)
                                if proc_code != "error":
                                    proc_code = separate_code(proc_code)
                                    if type(proc_code) == str and proc_code.strip() != "":
                                        lineError = proc_code
                                        procs[proc_name] = (tuple(params), [proc_code], list(filter(None, declarations)))
                                        procedimientos = procs
                                        #print(procedimientos)
                                        st = "\n--> Ejecucion finalizada debido a:\n--> ERROR SINTÁCTICO ~~~ " \
                                             "Ausencia de ';' en la linea " + str(get_line_error()) + "!☻"
                                        time.sleep(0.0005)
                                        return "error"
                                    if not verificar_ultimo(proc_code[-1]):
                                        lineError = proc_code[-1]
                                        #print(lineError)
                                        procs[proc_name] = (tuple(params), proc_code, list(filter(None, declarations)))
                                        procedimientos = procs
                                        #print(procedimientos)
                                        st = "\n--> Ejecucion finalizada debido a:\n--> ERROR SINTÁCTICO ~~~ " \
                                             "Ausencia de ';' en la linea " + str(get_line_error()) + "!☻"
                                        time.sleep(0.0005)
                                        return "error"
                                    values = (tuple(params), proc_code, list(filter(None, declarations)))
                                    procs[proc_name] = values
                                    code = code[count3 + 7:]
                                else:
                                    return "error"
                            else:
                                st = "\n--> Ejecucion finalizada debido a:\n--> ERROR SINTÁCTICO ~~~ " \
                                     "Error en PROC " + proc_name + " Estructura INICIO-FINAL incompleta☻"
                                time.sleep(0.0005)
                                return "error"
                        else:
                            st = "\n--> Ejecucion finalizada debido a:\n--> ERROR SINTÁCTICO ~~~ " \
                                 "Procedimiento sin nombre la estructura es: PROC <nombre>(<parametros>) FINPROC☻"
                            time.sleep(0.0005)
                            return "error name"
                    else:
                        st = "\n--> Ejecucion finalizada debido a:\n--> ERROR SINTÁCTICO ~~~" \
                             " Los parámetros del procedimiento deben encasillarse entre '( )'☻"
                        time.sleep(0.0005)
                        return "error"
            return procs


def get_code(code, is_proc):
    global st
    if code.count("INICIO") == code.count("FINAL"):
        if code[code.find("INICIO") + 6] == ":":
            if code.find("INICIO:") != -1 and code.find("FINAL;") != -1:
                if not is_proc:
                    if code.find("INICIO:") < code.find("FINAL;"):
                        if code[code.find("INICIO:"):code.find("FINAL;")].find("PROC") != -1:
                            if code.find("INICIO:") == -1:
                                st = "\n--> Ejecucion finalizada debido a:\n--> ERROR SINTÁCTICO ~~~ " \
                                     "La sentencia INICIO debe finalizar con ':'☻"
                                time.sleep(0.0005)
                                return "error"
                            else:
                                st = "\n--> Ejecucion finalizada debido a:\n--> ERROR SINTÁCTICO ~~~" \
                                     " La sentencia FINAL debe finalizar con ';'☻"
                                time.sleep(0.0005)
                                return "error"
                    else:
                        st = "\n--> Ejecucion finalizada debido a:\n--> ERROR SINTÁCTICO ~~~ " \
                             "La sentencia INICIO debe finalizar con ':'☻"
                        time.sleep(0.0005)
                        return "error"
                if code.index('INICIO:') < code.index('FINAL;'):
                    count1 = code.find("INICIO:")
                    blanco = code[:count1].replace("\n", " ").split()
                    if len(blanco) != 0 and not is_proc:
                        st = "\n--> Ejecucion finalizada debido a:\n--> ERROR SINTÁCTICO" \
                             " ~~~ Previo a INICIO del programa no debe existir código☻"
                        time.sleep(0.0005)
                        return "error"
                    count2 = code.index("FINAL;")
                    tr = code[(count1 + 7):count2]

                    return tr
                else:
                    st = "\n--> Ejecucion finalizada debido a:\n--> ERROR SINTÁCTICO ~~~ " \
                         "El programa debe encasillarse entre INICIO - FINAL en ese orden☻"
                    time.sleep(0.0005)
                    return "error"
            else:
                if code.find("INICIO:") == -1:
                    st = "\n--> Ejecucion finalizada debido a:\n--> ERROR SINTÁCTICO ~~~ " \
                         "La sentencia INICIO debe finalizar con ':'☻"
                    time.sleep(0.0005)
                    return "error"
                else:
                    st = "\n--> Ejecucion finalizada debido a:\n--> ERROR SINTÁCTICO ~~~" \
                         " La sentencia FINAL debe finalizar con ';'☻"
                    time.sleep(0.0005)
                    return "error"
        else:
            st = "\n--> Ejecucion finalizada debido a:\n--> ERROR SINTÁCTICO ~~~" \
                 " La sentencia INICIO debe finalizar con ':'☻"
            time.sleep(0.0005)
            return "error"
    else:
        st = "\n--> Ejecucion finalizada debido a:\n--> ERROR SINTÁCTICO ~~~ " \
             "Sentencia INICIO - FINAL incompleta☻"
        time.sleep(0.0005)
        return "error"


''' ------------------------------ ERRORES ------------------------------ '''


def get_line_error():
    global procedimientos
    global codigo
    global lineError
    global proc_called
    line_number = conteo_previo("INICIO")
    for i in codigo:
        for j in range(len(i)):
            #print()
            if lineError == i and not proc_called:
                while i[j] == "\n":
                    line_number += 1
                    j += 1
                return line_number
            if i[j] == "\n":
                line_number += 1
    for i in procedimientos:
        line_number = conteo_previo("PROC " + i)
        for j in procedimientos[i][2]:
            for k in range(len(j)):
                if lineError == j:
                    while j[k] == "\n":
                        line_number += 1
                        k += 1
                    return line_number
                if j[k] == "\n":
                    line_number += 1
        for j in procedimientos[i][1]:
            print(lineError, j)
            for k in range(len(j)):
                if lineError == j:
                    while j[k] == "\n":
                        line_number += 1
                        k += 1
                    return line_number
                if j[k] == "\n":
                    line_number += 1


def conteo_previo(to_evaluate):
    line_number = 1
    for i in range(len(prevCode[:prevCode.find(to_evaluate)])):
        if prevCode[i] == "\n":
            line_number += 1
    return line_number


''' ------------------------------ "CORRER" ------------------------------ '''


def runParser(code):
    global procedimientos
    global st
    global error
    global gvariables
    global flag_runnig
    global codigo
    global prevCode
    global lineError
    global buffer
    buffer = []
    prevCode = code
    codigo = get_code(code, False)
    error = False
    if codigo == "error":
        error = True
        flag_runnig = False
        return
    procs = get_proc(code)
    if type(procs) == str:
        error = True
        flag_runnig = False
        return
    procedimientos = procs
    codigo = separate_code(codigo)
    if not verificar_ultimo(codigo[-1]):
        lineError = codigo[len(codigo) - 1]
        st = "\n--> Ejecucion finalizada debido a:\n--> ERROR SINTÁCTICO ~~~ " \
             "Ausencia de ';' en la linea " + str(get_line_error()) + "☻"
        time.sleep(0.0005)
        flag_runnig = False
        return
    if type(codigo) == str:
        codigo = [codigo, ]

    for i in codigo:
        time.sleep(0.0005)
        lineError = i
        result = parse_code(i.replace("\n", " "))
        if len(result[0]) > 0:
            st += result[0]
        if result[1]:
            if 'ejecución' not in st:
                st = "\n--> Ejecucion finalizada debido a:" + st + "☻"
            break
        time.sleep(0.00001)
        st = ""
    gvariables.clear()
    time.sleep(0.0005)
    if st == "":
        st = "\n--> Ejecucion finalizada☺"
        logic.bluetooth.send(buffer)
    time.sleep(0.00001)
    flag_runnig = False


def verificar_ultimo(ultima):
    for i in ultima:
        if i != "\n" and i != " ":
            return False
    return True
