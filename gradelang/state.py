""" gradelang State.
"""


class State:
    def __init__(self):
        self.symbol_table: dict
        self.ast: list
        self.initialize()

    def initialize(self):
        # symbol table to hold variable-value associations
        self.symbol_table = {}

        # when done parsing this variable will hold our AST
        self.AST = None


state = State()
