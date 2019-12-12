""" gradelang State.
"""
import json
from typing import List

from gradelang.question import Question


class State:
    symbol_table: dict
    setup: tuple
    _questions: List[Question]
    teardown: tuple
    output: list

    question: Question

    def __init__(self):
        self.clean()

    def reset(self):
        self.symbol_table = dict()
        return

    def clean(self):
        self.reset()
        self.setup = tuple()
        self._questions = list()
        self.teardown = tuple()
        self.output = list()
        return

    @property
    def questions(self):
        yield from self._questions

    def add_question(self, name, body):
        self._questions.append(
            Question(
                name=name if name != ('nil',) else len(self._questions),
                body=body,
            )
        )
        return

    def score(self):
        return sum(q.score for q in self.questions)

    def max_score(self):
        return sum(q.max_score for q in self.questions)

    def json(self):
        return json.dumps(
            {
                'tests': [q.json() for q in self.questions]
            },
            indent=4
        )

    def markdown(self):
        return '\n'.join(filter(lambda x: x, [
            '# Results',
            f'## Score: {self.score()}/{self.max_score()}',
            *[q.markdown() for q in self.questions]
        ]))

    def report(self):
        return '\n'.join(filter(lambda x: x, [
            'Grade Results',
            *[q.report() for q in self.questions]
        ]))


state = State()
