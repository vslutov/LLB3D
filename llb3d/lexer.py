# -*- coding: utf-8 -*-

"""Lexer for Blitz3D language."""

from ply import lex

import re

class g:
    lexer = None
    parser = None
    error_list = None
    code = None

    def input(code):
        if g.lexer is None:
            g.lexer = lex.lex()
        g.error_list = []

        g.code = code
        g.lexer.input(code.upper())
        g.lexer.lineno = 1

literals = '#$%(),.\\=\n+-~^*/<>'

keywords = [
    'AFTER', 'AND', 'BEFORE', 'CASE', 'CONST', 'DATA', 'DEFAULT', 'DELETE',
    'DIM', 'EACH', 'ELSE', 'ELSEIF', 'END', 'ENDIF', 'EXIT', 'FALSE',
    'FIELD', 'FIRST', 'FLOAT', 'FOR', 'FOREVER', 'FUNCTION', 'GLOBAL',
    'GOSUB', 'GOTO', 'IF', 'INSERT', 'INT', 'LAST', 'LOCAL', 'MOD', 'NEW',
    'NEXT', 'NOT', 'NULL', 'OR', 'PI', 'READ', 'REPEAT', 'RESTORE', 'RETURN',
    'SAR', 'SELECT', 'SHL', 'SHR', 'STEP', 'STR', 'THEN', 'TO', 'TRUE',
    'TYPE', 'UNTIL', 'WEND', 'WHILE', 'XOR', 'INCLUDE'
]

# List of token names.   This is always required
tokens = [
    'FLOATVAL', 'INTVAL', 'STRVAL',
    'ID',
] + keywords

def find_column(lexpos):
    last_cr = g.code.rfind('\n', 0, lexpos)
    if last_cr == -1:
        return lexpos + 1
    else:
        return lexpos - last_cr

def position(t):
    return '{line}:{col}'.format(line=t.lineno,
                                 col=find_column(t.lexpos))

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t\r\f\v'
t_ignore_COMMENT = r';.*'

def t_FLOATVAL(t):
    r'(?:\d+\.\d*)|(?:\.\d+)'
    t.value = float(t.value)
    return t

def t_INTVAL(t):
    r'\d+'
    t.value = int(t.value, 0)
    return t

def t_STRVAL(t):
    r'".*?"'
    length = len(t.value) - 2
    t.value = g.code[t.lexpos + 1:t.lexpos + 1 + length]
    return t

# A regular expression rule with some action code
def t_ID(t):
    r'\w+'
    if t.value in keywords:
        t.type = t.value
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n'
    t.lexer.lineno += 1
    t.type = '\n'
    return t

# Error handling rule
def t_error(t):
    g.error_list.append("Illegal character '{char}' at {position}"
                        .format(char=t.value[0], position=position(t)))
    g.lexer.skip(1)

def get_lexems(code):
    """Get array of lexems and errors."""

    g.input(code)
    result = list(g.lexer)
    return g.error_list, result
