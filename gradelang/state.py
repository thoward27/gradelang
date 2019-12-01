""" gradelang State.
"""
from typing import List

from gradelang.question import Question
from gradelang.results import Results


class State:
    symbol_table: dict
    setup: tuple
    _questions: List[Question]
    teardown: tuple
    output: tuple
    results: Results

    def __init__(self):
        self.reset()

    def reset(self):
        self.symbol_table = dict()
        self.setup = tuple()
        self._questions = list()
        self.teardown = tuple()
        self.output = tuple()
        return

    @property
    def questions(self):
        yield from self._questions

    def add_question(self, name, body):
        self._questions.append(
            Question(
                name=name if name != ('nil',) else len(self._questions),
                body=body,
                # TODO: Can we sum all possible points? AKA # of AWARD statements?
                value=0
            )
        )
        return

    def update_results(self, results):
        self.results = results


state = State()
