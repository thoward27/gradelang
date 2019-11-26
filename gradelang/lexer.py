""" gradelang Lexer.
"""

reserved = {
    'setup': 'SETUP',
    'teardown': 'TEARDOWN',
    'save': 'SAVE',
    'question': 'QUESTION',
    'worth': 'WORTH',
    'assert': 'ASSERT',
    'let': 'LET',
    'assume': 'ASSUME',
    'be': 'BE',
    'a': 'A',
    'String': 'STRING_TYPE',
    'Program': 'PROGRAM_TYPE',
}

literals = ['=', '(', ')', ',', '{', '}', ';']

tokens = [
     'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
     'EQ', 'LE', 'AND', 'OR', 'NOT',
     'INTEGER', 'ID', 'STRING',
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
t_INTEGER = r'[0-9]+'

t_ignore = ' \t'


def t_ID(t):
    r"""[a-zA-Z][a-zA-Z_0-9]*"""
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t


def t_STRING(t):
    r"""\"[^\"]*\""""
    t.value = t.value[1:-1]  # strip the quotes
    return t


def t_COMMENT(_):
    r"""\#.*"""
    pass


def t_NEWLINE(t):
    r"""\n"""
    t.lexer.lineno += len(t.value)
    pass


def t_error(t):
    raise SyntaxError(f'Illegal character: {t}')
