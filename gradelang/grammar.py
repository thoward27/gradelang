""" Grammar construction.

.. code-block:: none

    prog :
        blocks
        | empty

    blocks : 
        block blocks
        | empty

    block : 
        SETUP '{' statements '}'
        | QUESTION opt_name opt_given '{' statements '}'
        | TEARDOWN '{' statements '}'
        | OUTPUT '{' outputs '}'

    statement :
        type NAME '=' exp
        | NAME '(' parameters ')'
        | REQUIRE STRING strings
        | RUN args 
        | ASSERT exp
        | CHECK exp
        | PRINT exp
        | AWARD exp 

    given :
        GIVEN question_parameters
    
    question_parameter: NAME '=' type '(' parameters ')'

    output : 
        JSON opt_string
        | MARKDOWN opt_string

    arg : exp
    kwarg : NAME '=' exp

    exp : 
        exp math_op exp
        | exp comparator exp
        | exp AND exp
        | exp OR exp
        | NOT exp
        | EXIT INTEGER 
        | exp IN output 
        | exp NOT IN output 
        | INTEGER
        | NAME
        | STRING
        | MINUS exp %prec UMINUS
        | '(' exp ')'

    math_op : PLUS | MINUS | TIMES | DIVIDE

    comparator : EQ | LE | LT | GE | GT

    output : STDOUT | STDERR
    
    type : String | Int | Float

    statements : 
        statement ';' statements
        | empty

    strings : 
        STRING
        | STRING ',' strings
        | empty
    
    parameters :
        args kwargs | empty

    question_parameters : 
        question_parameter
        | question_parameter ',' question_paramaters
        | empty

    outputs : 
        output ';' outputs 
        | empty
        
    args:
        arg
        | arg ',' args
        | empty

    kwargs:
        kwarg
        | kwarg ',' kwargs
        | empty
  
    opt_name : INTEGER | STRING | empty
    opt_given : given | empty
    opt_string : STRING | empty

TODO Pull lexer tokens in?
"""
from .lexer import *
from .state import state, NIL

#########################################################################
# set precedence and associativity
# NOTE: all operators need to have tokens
#       so that we can put them into the precedence table
precedence = (
    ('left', 'AND', 'OR'),
    ('left', 'EQ', 'LE', 'LT', 'GE', 'GT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS', 'NOT')
)


#########################################################################
# grammar rules with embedded actions
#########################################################################
def p_prog(_):
    """
    prog : blocks 
        | empty
    """
    pass


def p_blocks(_):
    """
    blocks : block blocks
        | empty
    """
    pass


def p_block(p):
    """
    block : SETUP '{' statements '}'
          | QUESTION opt_name '{' statements '}'
          | TEARDOWN '{' statements '}'
          | OUTPUT '{' outputs '}'
    """
    if p[1] == 'setup':
        state.setup = p[3]

    elif p[1] == 'question':
        state.add_question(name=p[2], body=p[4])

    elif p[1] == 'teardown':
        state.teardown = p[3]

    elif p[1] == 'output':
        state.output = p[3]

    else:
        raise ValueError(f'Unexpected block: {p[1]}')


def p_statement(p):
    """
    statement : type NAME '=' exp
        | NAME '(' parameters ')'
        | REQUIRE STRING strings
        | RUN args 
        | ASSERT exp
        | CHECK exp
        | AWARD exp
    """
    if len(p) == 4 and p[3] == '=':
        if p[1] in types.keys():
            p[0] = ('assign', p[1], p[2], p[4])
        else:
            raise ValueError(f'Unexpected type {p[1]}')

    elif isinstance(p[1], tuple) and p[1][0] == 'name':
        p[0] = ('call', p[1], p[3])
    
    elif p[1] == 'require':
        p[0] = ('require', p[2], p[3])

    elif p[1] in {'run', 'assert', 'check', 'award'}:
        p[0] = (p[1], p[2])

    else:
        raise ValueError(f"Unexpected symbol {p[1]}")


def p_given(p):
    """
    given : GIVEN question_parameters
    """
    p[0] = ('given', p[1])


def p_question_parameter(p):
    """
    question_parameter : NAME '=' type '(' parameters ')'
    """
    p[0] = (p[1], p[3], p[5])


def p_output(p):
    """
    output : JSON opt_string
        | MARKDOWN opt_string
    """
    p[0] = {p[1]: p[2]}


def p_arg(p):
    """
    arg : exp
    """
    p[0] = p[1]


def p_kwarg(p):
    """
    kwarg : NAME '=' exp
    """
    p[0] = (p[1], p[3])


###
# Expressions
###

def p_binop_exp(p):
    """
    exp : exp math_op exp
        | exp comparator exp
        | exp AND exp
        | exp OR exp
        | exp IN output 
        | exp NOT IN output 
    """
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    elif p[2:4] == ['not', 'in']:
        p[0] = ('notin', p[1], p[3])

def p_uminus_exp(p):
    """
    exp : MINUS exp %prec UMINUS
    """
    p[0] = ('uminus', p[2])


def p_not_exp(p):
    """
    exp : NOT exp
    """
    p[0] = ('not', p[2])

def p_unary_exp(p):
    """
    exp : EXIT INTEGER 
        | NOT exp
    """
    p[0] = (p[1], p[2])

def p_integer_exp(p):
    """
    exp : INTEGER
    """
    p[0] = ('integer', int(p[1]))


def p_float_exp(p):
    """
    exp : FLOAT
    """
    p[0] = ('float', float(p[1]))


def p_name_exp(p):
    """
    exp : NAME
    """
    p[0] = ('name', p[1])


def p_string_exp(p):
    """
    exp : STRING
    """
    p[0] = ('string', p[1])


def p_paren_exp(p):
    """
    exp : '(' exp ')'
    """
    p[0] = ('paren', p[2])


def p_math_op(p):
    """
    math_op : PLUS
        | MINUS
        | TIMES
        | DIVIDE
    """
    p[0] = p[1]


def p_comparator(p):
    """
    comparator : EQ
        | LE
        | LT
        | GE
        | GT
    """
    p[0] = p[1]


def p_output(p):
    """
    output : STDOUT
        | STDERR
    """
    p[0] = p[1]


def p_type(p):
    """
    type : String
         | Int
         | Float
    """
    p[0] = p[1]


###
# List of things.
###

def p_statements(p):
    """
    statements : statement ';' statements
        | empty
    """
    if len(p) == 4:
        p[0] = ('seq', p[1], p[3])

    elif len(p) == 2:
        p[0] = p[1]


def p_strings(p):
    """
    strings : ',' STRING strings
        | empty
    """
    if len(p) == 4:
        p[0] = (p[2], *p[3])
    else:
        p[0] = (p[1],)


def p_parameters(p):
    """
    parameters : param ',' parameters
        | param
        | empty
    """
    if len(p) == 4:
        p[0] = (p[1], *p[3])
    else:
        p[0] = (p[1],)


def p_question_parameters(p):
    """
    question_parameters : question_parameter
        | question_parameter ',' question_parameters
        | empty
    """
    # TODO
    p[0] = p[1]


def p_outputs(p):
    """
    outputs : output ';' outputs
        | empty
    """
    if len(p) >= 3:
        # If we have at least one format, filter out the empty tag,
        # we do this, because presence of the empty tag will cause
        # the output of the default report format, regardless of
        # user-specified choices.
        p[0] = {**p[1], **{fmt: file for fmt, file in p[3].items() if fmt != NIL}}
    elif len(p) == 2:
        p[0] = {p[1]: ''}


def p_args(p):
    """
    args : arg
        | arg ',' args
        | empty
    """
    # TODO
    p[0] = p[1]


def p_kwargs(p):
    """
    kwargs : kwarg
        | kwarg ',' kwargs
        | empty
    """
    p[0] = p[1]


def p_opt_name(p):
    """
    opt_name : INTEGER
         | STRING
         | empty
    """
    p[0] = p[1]


def p_opt_given(p):
    """
    opt_given : given
        | empty
    """
    p[0] = p[1]


def p_opt_string(p):
    """
    opt_string : STRING
               | empty
    """
    p[0] = p[1]


def p_empty(p):
    """
    empty :
    """
    p[0] = NIL


def p_error(t):
    raise SyntaxError(str(t))
