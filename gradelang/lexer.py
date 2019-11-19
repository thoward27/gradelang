""" gradelang Lexer.
"""

reserved = {
    'input': 'INPUT',
    'print': 'PRINT',
    'end': 'END',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'endif': 'ENDIF',
    'while': 'WHILE',
    'endwhile': 'ENDWHILE',
    'for': 'FOR',
    'to': 'TO',
    'step': 'STEP',
    'next': 'NEXT'
}

literals = ['=', '(', ')', ',']

tokens = [
             'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
             'EQ', 'LE', 'AND', 'OR', 'NOT',
             'INTEGER', 'ID', 'STRING'
         ] + list(reserved.values())

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQ = r'=='
t_LE = r'<='
t_AND = r'\&'
t_OR = r'\|'
t_NOT = r'!'

t_ignore = ' \t'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t


def t_INTEGER(t):
    r'[0-9]+'
    return t


def t_STRING(t):
    r'\"[^\"]*\"'
    t.value = t.value[1:-1]  # strip the quotes
    return t


def t_COMMENT(t):
    r'\'.*'
    pass


def t_NEWLINE(t):
    r'\n'
    pass


def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)
