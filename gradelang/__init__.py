__all__ = ['lexer', 'parser']

from ply import lex, yacc

from .grammar import *
from .lexer import *

lexer = lex.lex()
parser = yacc.yacc()
