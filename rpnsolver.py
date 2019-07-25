# -*- coding: utf-8 -*-

import ply.lex as lex
import ply.yacc as yacc
import math

variables = {}

#      _
#     | |
#     | |     _____  _____ _ __
#     | |    / _ \ \/ / _ \ '__|
#     | |___|  __/>  <  __/ |
#     \_____/\___/_/\_\___|_|
#
multiplier = {'T': 1e12, 'G': 1e9, 'M': 1e6, 'k': 1e3, 'm': 1e-3, 'u': 1e-6, 'n': 1e-9, 'p': 1e-12, 'f': 1e-15}
constants = {'PI': math.pi, 'E': math.e, 'C': 299792458}

class VariableError(Exception): pass
class LexError(Exception): pass
class ConstantError(Exception): pass
class GrammarError(Exception): pass

# literals = ['\n']

reserved = {
    'dup': 'DUP',
    # 'swap': 'SWAP',
    'sin': 'SIN', 'cos': 'COS', 'tan': 'TAN',
    'asin': 'ASIN', 'acos': 'ACOS', 'atan': 'ATAN',
    'sqr': 'SQR',
    'sqrn': 'SQRN',
    'rad': 'RAD', 'deg': 'DEG',
    # 'log': 'LOG', 'ln': 'LN',
    }
tokens = ['ASSIGN', 'NUMBER', #'MULTIPLIER',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    # 'LPAREN', 'RPAREN',
    'POWER',
    'ESCAPE', #'FILTER',
    'EOL',
    'ID'
    ]+list(reserved.values())

t_ignore     = " \t"
t_PLUS       = r'\+'
t_MINUS      = r'-'
t_TIMES      = r'\*'
t_DIVIDE     = r'/'
# t_LPAREN     = r'\('
# t_RPAREN     = r'\)'
t_POWER      = r'\^'
t_ASSIGN     = r'='
t_ESCAPE     = r'!'
# t_FILTER     = r'\|'
# t_MULTIPLIER = r'T|G|M|k|m|u|n|p'

def t_comment(t):
    r'\#[^\n]*'
    pass

def t_EOL(t):
    r'\n'
    t.lexer.lineno += t.value.count("\n")
    # print(t.lexer.lineno)
    return t

def t_ID(t):
    r'[a-z][a-z0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'(?:(?:\d+(?:[.,]\d+)?)|(?:[.,]\d+))(?:(?:[Ee][+-]?\d+)|T|G|M|k|m|u|n|p|f)?'
    try:
        v = t.value.translate({ord(','): '.'})
        if v[-1] in multiplier.keys():
            t.value = float(v[:-1])*multiplier[v[-1]]
        else:
            t.value = float(v)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_error(t):
    # print("Illegal character '%s'" % t.value[0])
    # t.lexer.skip(1)
    raise LexError(t)


#     ______
#     | ___ \
#     | |_/ /_ _ _ __ ___  ___ _ __
#     |  __/ _` | '__/ __|/ _ \ '__|
#     | | | (_| | |  \__ \  __/ |
#     \_|  \__,_|_|  |___/\___|_|
#
# precedence = (
#     ('right', 'ASSIGN'),
#     # ('right', 'ID'),
#     ('left', 'PLUS', 'MINUS'),
#     ('right', 'SIN', 'COS', 'TAN', 'ASIN', 'ACOS', 'ATAN'),
#     ('right', 'DEG', 'RAD'),
#     ('left', 'TIMES', 'DIVIDE'),
#     ('left', 'SQR'),
#     ('left', 'POWER'),
#     ('right', 'UMINUS', 'FILTER'),
#     ('nonassoc', 'ESCAPE'),
#     )

def p_result(p):
    'result : list'
    p[0] = p[1]

def p_list_null(p):
    '''list : EOL'''
    s = (p.lexer.lineno, None)
    p[0] = [s]

def p_list(p):
    '''list : statment EOL'''
    s = (p.lexer.lineno, p[1])
    p[0] = [s]

def p_list_stat(p):
    '''list : list statment EOL'''
    s = (p.lexer.lineno, p[2])
    p[0] = p[1]+[s]

def p_statement_none(p):
    '''statment :'''
    p[0] = None

def p_statement(p):
    '''statment : value'''
    p[0] = p[1]

def p_assign(p):
    '''value : ID ASSIGN value'''
    p[0] = p[3]
    variables[p[1]] = p[3]

def p_val_binop(p):
    '''value : value value PLUS
             | value value MINUS
             | value value TIMES
             | value value DIVIDE'''
    if   p[3] == '+': p[0] = p[1] + p[2]
    elif p[3] == '-': p[0] = p[1] - p[2]
    elif p[3] == '*': p[0] = p[1] * p[2]
    elif p[3] == '/': p[0] = p[1] / p[2]

# def p_val_uminus(p):
#     'value : value MINUS'
#     p[0] = -p[1]

def p_val_angle(p):
    '''value : value RAD
             | value DEG'''
    if p[2] == 'rad': p[0] = p[1]*math.pi/180.0
    else: p[0] = p[1]*180.0/math.pi

def p_val_trig(p):
    '''value : value SIN
             | value COS
             | value TAN'''
    if   p[2] == 'sin': p[0] = math.sin(p[1])
    elif p[2] == 'cos': p[0] = math.cos(p[1])
    elif p[2] == 'tan' : p[0] = math.tan(p[1])

def p_val_atrig(p):
    '''value : value ASIN
             | value ACOS
             | value ATAN'''
    if   p[2] == 'asin': p[0] = math.asin(p[1])
    elif p[2] == 'acos': p[0] = math.acos(p[1])
    elif p[2] == 'atan' : p[0] = math.atan(p[1])

def p_val_power(p):
    '''value : value value POWER'''
    p[0] = math.pow(p[1], p[2])

def p_val_square(p):
    '''value : value SQR'''
    p[0] = math.sqrt(p[1])

def p_val_square_ex(p):
    '''value : value value SQRN'''
    p[0] = math.pow(p[1], 1./p[2])

# def p_val_group(p):
#     'value : LPAREN value RPAREN'
#     p[0] = p[2]

# def p_val_number_multi(p):
#     'value : NUMBER ID'
#     p[0] = p[1]*multiplier[p[2]]

def p_dup(p):
    'value : DUP'
    p[0] = p[-1]
# def p_dup(p):
#     'value : value DUP'
#     p[0] = p[1]

# def p_empty(p):
#     'empty :'
#     pass

# def p_swap(p):
#     'empty : SWAP'
#     p[-1], p[-2] = p[-2], p[-1]
#     # p[0] = None
# def p_swap(p):
#     'value : value value SWAP'
#     p[-1], p[-2] = p[-2], p[-1]
#     # p[0] = None
# def p_swap(p):
#     'value  : value value SWAP'
#     # 'value value : value value SWAP'
#     print(p[-1], p[0], p[1])
#     p[0] = p[1]
#     # p[1] = p[2]
#     # print(type(p))
#     # p[-1] = p[1]
#     print(p[-1], p[0], p[1])
#     # p[-1], p[-2] = p[-2], p[-1]
#     # p[0] = None

def p_val_number(p):
    'value : NUMBER'
    p[0] = p[1]

def p_variable(p):
    'value : ID'
    p[0] = variables.get(p[1], 0)
    # TODO avisar se nao existir

def p_scaped(p):
    'value : ESCAPE ID'
    p[0] = 0
    if p[2] == 'pi': p[0] = math.pi
    if p[2] == 'e': p[0] = math.e

def p_error(p):
    # print("Syntax line %d, at '%s'" % (p.lineno, p.value))
    raise GrammarError(p)
    # raise TypeError("unknown text at %r" % (p.value,))

#     global flag_for_error
#     flag_for_error = 1

#     if p is not None:
#         errors_list.append("Erreur de syntaxe à la ligne %s"%(p.lineno))
#         yacc.errok()
#     else:
#         print("Unexpected end of input")


#      _   _      _
#     | | | |    | |
#     | |_| | ___| |_ __   ___ _ __
#     |  _  |/ _ \ | '_ \ / _ \ '__|
#     | | | |  __/ | |_) |  __/ |
#     \_| |_/\___|_| .__/ \___|_|
#                  | |
#                  |_|

dev = False


lexer = lex.lex(lextab='rpnsolver_lex', optimize=not dev, debug=dev)
parser = yacc.yacc(tabmodule='rpnsolver_tab', optimize=not dev, debug=dev)

def solve(text):
    global variables
    variables = {}
    lexer.lineno = 0
    return parser.parse(text+'\n', lexer=lexer, debug=dev, tracking=True)

#      _____         _
#     |_   _|       | |
#       | | ___  ___| |_ ___ _ __
#       | |/ _ \/ __| __/ _ \ '__|
#       | |  __/\__ \ ||  __/ |
#       \_/\___||___/\__\___|_|
#
if __name__ == '__main__':

    import cmd

    class MeuTeste(cmd.Cmd):
        """MeuTeste """

        def __init__(self):
            cmd.Cmd.__init__(self)
            self.prompt = "mt> "
            self.intro  = "Executando o MeuTeste"

        def do_exit(self, args):
            return -1

        def do_EOF(self, args):
            return self.do_exit(args)

        def emptyline(self):
            pass

        def default(self, line):
            print('>>>> ', parser.parse(line+'\n', lexer=lexer, debug=dev, tracking=True))

    mt = MeuTeste()
    mt.cmdloop()
