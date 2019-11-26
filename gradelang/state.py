""" gradelang State.
"""


class State:
    symbol_table: dict
    setup: list
    questions: list
    teardown: list

    AST: list

    def __init__(self):
        self.reset()

    def reset(self):
        self.symbol_table = dict()
        self.setup = list()
        self.questions = list()
        self.teardown = list()
        self.AST = list()


state = State()
