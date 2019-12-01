""" gradelang State.
"""


class State:
    symbol_table: dict
    setup: tuple
    questions: list
    teardown: tuple
    output: tuple

    def __init__(self):
        self.reset()

    def reset(self):
        self.symbol_table = dict()
        self.setup = tuple()
        self.questions = list()
        self.teardown = tuple()
        self.output = tuple()


state = State()
