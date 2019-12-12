""" gradelang Lexer.
"""

types = {
    'String': 'String',
    'Int': 'Int',
    'Float': 'Float',
}

outputs = {
    'json': 'JSON',
    'markdown': 'MARKDOWN'
}

builtins = {
    'assert': 'ASSERT',
    'assume': 'ASSUME',
    'print': 'PRINT',
    'exit': 'EXIT',
    'stdout': 'STDOUT',
    'stderr': 'STDERR',
    'successful': 'SUCCESSFUL',
    'failure': 'FAILURE',
    'run': 'RUN',
}

blocks = {
    'setup': 'SETUP',
    'question': 'QUESTION',
    'teardown': 'TEARDOWN',
    'output': 'OUTPUT',
}

stmts = {
    'let': 'LET',
    'award': 'AWARD',
    'in': 'IN',
    'be': 'BE',
}

logical = {
    'not': 'NOT',
    'and': 'AND',
    'or': 'OR',
}

reserved = {
    **types,
    **builtins,
    **blocks,
    **stmts,
    **outputs,
    **logical,
}

literals = ['=', '>', '<', '(', ')', ',', '{', '}', ';']

tokens = [
    # Mathematical
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    # Equality
    'EQ', 'LE', 'GE', 'LT', 'GT',
    # Logical
    # 'AND', 'OR', 'NOT',
    # Primitives
    'STRING', 'FLOAT', 'INTEGER',
    # Other
    'ID',
    *list(reserved.values())
]

# Mathematical
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
# Equality
t_EQ = r'=='
t_LE = r'<='
t_LT = r'<'
t_GE = r'>='
t_GT = r'>'


# Logical
# t_AND = r'\&'
# t_OR = r'\|'
# t_NOT = r'not'


def t_FLOAT(t):
    r"""-?[0-9]+\.[0-9]+"""
    return t


def t_INTEGER(t):
    r"""-?[0-9]+"""
    return t


def t_ID(t):
    r"""[a-zA-Z_][a-zA-Z_0-9]*"""
    # Check for reserved words
    t.type = reserved.get(t.value, 'ID')
    return t


def t_STRING(t):
    r"""(\"[^"]*\")|(\'[^']*\')"""
    t.value = t.value[1:-1]  # strip the quotes
    return t


# def t_PARAM_ASSIGN(t):
#    r"""[a-zA-Z_]+\=[a-zA-Z_0-9]+"""
#    #t.type = reserved.get(t.value, "PARAM_ASSIGN")
#    return t


def t_NEWLINE(t):
    r"""\n"""
    t.lexer.lineno += len(t.value)
    pass


def t_error(t):
    raise SyntaxError(f'Illegal character: {t}')


t_ignore = ' \t'
t_ignore_COMMENT = r'\#.*'
