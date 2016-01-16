# -*- coding: utf-8 -*-

import ply.lex as lex
import ply.yacc as yacc
import cmd
import math

optimize = False
debug = True

#      _
#     | |
#     | |     _____  _____ _ __
#     | |    / _ \ \/ / _ \ '__|
#     | |___|  __/>  <  __/ |
#     \_____/\___/_/\_\___|_|
#

reserved = {
    'sin': 'SIN',
    'cos': 'COS',
    'tan': 'TAN',
    'asin': 'ASIN',
    'acos': 'ACOS',
    'atan': 'ATAN',
    'sqr': 'SQR',
    'rad': 'RAD',
    'deg': 'DEG',
    }
tokens = ['NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN', 'POWER', 'ID']+list(reserved.values())

t_ignore = " \t"
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_POWER   = r'\^'

def t_ID(t):
    r'[a-z]+'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'(?:\d+(?:[.,]\d+)?)|(?:[.,]\d+)'
    try:
        # TODO fazer aceitar virgula
        t.value = float(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex(optimize=optimize, debug=debug)

#     ______
#     | ___ \
#     | |_/ /_ _ _ __ ___  ___ _ __
#     |  __/ _` | '__/ __|/ _ \ '__|
#     | | | (_| | |  \__ \  __/ |
#     \_|  \__,_|_|  |___/\___|_|
#
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('right', 'SIN', 'COS', 'TAN', 'ASIN', 'ACOS', 'ATAN'),
    ('right', 'DEG', 'RAD'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'SQR'),
    ('left', 'POWER'),
    ('right', 'UMINUS'),
    )

def p_statement_expr(t):
    'result : value'
    t[0] = t[1]

def p_val_binop(t):
    '''value : value PLUS value
             | value MINUS value
             | value TIMES value
             | value DIVIDE value'''
    if   t[2] == '+': t[0] = t[1] + t[3]
    elif t[2] == '-': t[0] = t[1] - t[3]
    elif t[2] == '*': t[0] = t[1] * t[3]
    elif t[2] == '/': t[0] = t[1] / t[3]

def p_val_uminus(t):
    'value : MINUS value %prec UMINUS'
    t[0] = -t[2]

def p_val_angle(t):
    '''value : RAD value
             | DEG value'''
    if t[1] == 'rad': t[0] = t[2]*math.pi/180.0
    else: t[0] = t[2]*180.0/math.pi

def p_val_trig(t):
    '''value : SIN value
             | COS value
             | TAN value'''
    if   t[1] == 'sin': t[0] = math.sin(t[2])
    elif t[1] == 'cos': t[0] = math.cos(t[2])
    elif t[1] == 'tan' : t[0] = math.tan(t[2])

def p_val_atrig(t):
    '''value : ASIN value
             | ACOS value
             | ATAN value'''
    if   t[1] == 'asin': t[0] = math.asin(t[2])
    elif t[1] == 'acos': t[0] = math.acos(t[2])
    elif t[1] == 'atan' : t[0] = math.atan(t[2])

def p_val_power(t):
    '''value : value POWER value'''
    t[0] = math.pow(t[1], t[3])

def p_val_square(t):
    '''value : SQR value'''
    t[0] = math.sqrt(t[2])

def p_val_group(t):
    'value : LPAREN value RPAREN'
    t[0] = t[2]

def p_val_number(t):
    'value : NUMBER'
    t[0] = t[1]

def p_error(t):
    print("Syntax error at '%s'" % t.value)

parser = yacc.yacc(optimize=optimize, debug=debug)

#      _____         _
#     |_   _|       | |
#       | | ___  ___| |_ ___ _ __
#       | |/ _ \/ __| __/ _ \ '__|
#       | |  __/\__ \ ||  __/ |
#       \_/\___||___/\__\___|_|
#

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
        print '>>>> ', parser.parse(line, debug=debug)

if __name__ == '__main__':
    mt = MeuTeste()
    mt.cmdloop()
