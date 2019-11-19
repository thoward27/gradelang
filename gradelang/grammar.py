""" gradelang Grammar.
"""

from ply import yacc

# set precedence and associativity
precedence = (
    ('left', 'AND', 'OR'),
    ('left', 'EQ', 'LE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS', 'NOT')
)


def p_grammar(_):
    """
    prog : stmt_list
    
    stmt_list : stmt stmt_list
              | stmt

    stmt : ID '=' exp
         | INPUT opt_string ID
         | PRINT value value_list
         | END
         | IF exp THEN stmt_list opt_else ENDIF
         | WHILE exp stmt_list ENDWHILE
         | FOR ID '=' exp TO exp opt_step stmt_list NEXT ID
    
    opt_string : STRING ','
               | empty
               
    value_list : ',' value value_list
               | empty
               
    opt_else : ELSE stmt_list
             | empty
             
    opt_step : STEP exp
             | empty

    exp : exp PLUS exp
        | exp MINUS exp
        | exp TIMES exp
        | exp DIVIDE exp
        | exp EQ exp
        | exp LE exp
        | exp AND exp
        | exp OR exp
        | INTEGER
        | ID
        | '(' exp ')'
        | MINUS exp %prec UMINUS
        | NOT exp

    value : ID
          | INTEGER
          | STRING
    """
    pass


def p_empty(p):
    'empty :'
    pass


def p_error(t):
    raise SyntaxError(f"Syntax error at '{t.value}'")


# build the parser
parser = yacc.yacc()
