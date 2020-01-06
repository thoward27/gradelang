""" Gradelang Lexer.
"""

# Builtin types, all supporting automated generation.
types = {
    'String': 'String',
    'Int': 'Int',
    'Float': 'Float',
}

# Supported output formats.
outputs = {
    'json': 'JSON',
    'markdown': 'MARKDOWN'
}

# Builtin functions.
builtins = {
    'assert': 'ASSERT',
    'check': 'CHECK',
    'print': 'PRINT',
    'award': 'AWARD',
    'run': 'RUN',
    'require': 'REQUIRE',
}

# Supported control blocks.
blocks = {
    'setup': 'SETUP',
    'question': 'QUESTION',
    'teardown': 'TEARDOWN',
    'output': 'OUTPUT',
}

# Assorted keywords.
keywords = {
    'in': 'IN',
    'exit': 'EXIT',
    'stdout': 'STDOUT',
    'stderr': 'STDERR',
    'given': 'GIVEN',
}

# Logical operators.
logical = {
    'not': 'NOT',
    'and': 'AND',
    'or': 'OR',
}

# Here, we build the full dictionary of reserved words.
reserved = {
    **types,
    **builtins,
    **blocks,
    **outputs,
    **logical,
    **keywords
}

literals = ['=', '>', '<', '(', ')', ',', '{', '}', ';']

tokens = [
    # Mathematical
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    # Equality
    'EQ', 'LE', 'GE', 'LT', 'GT',
    # Primitives
    'STRING', 'FLOAT', 'INTEGER',
    # Other
    'NAME',
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


def t_FLOAT(t):
    r"""-?[0-9]+\.[0-9]+"""
    return t


def t_INTEGER(t):
    r"""-?[0-9]+"""
    return t


def t_NAME(t):
    r"""[a-zA-Z_][a-zA-Z_0-9]*"""
    # Check for reserved words
    t.type = reserved.get(t.value, 'ID')
    return t


def t_STRING(t):
    r"""(\"[^"]*\")|(\'[^']*\')"""
    t.value = t.value[1:-1]  # strip the quotes
    return t


def t_NEWLINE(t):
    r"""\n"""
    t.lexer.lineno += len(t.value)


def t_error(t):
    raise SyntaxError(f'Illegal character: {t}')


t_ignore = ' \t'
t_ignore_COMMENT = r'\#.*'
