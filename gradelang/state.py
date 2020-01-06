""" State manager.
"""
import json
import threading
from typing import List
import warnings
from functools import cached_property

from gradelang.question import Question

NIL = ('nil',)

thread_storage = threading.local()

class State:
    symbol_table: dict
    setup: tuple
    _questions: List[Question]
    teardown: tuple
    output: dict

    def __init__(self):
        self.reset()

    def __getitem__(self, index: int) -> Question:
        return self._questions[index]

    def reset(self):
        self.symbol_table = {}
        self.reset()
        self.setup = NIL
        self._questions = list()
        self.teardown = NIL
        self.output = {NIL: ''}

    def clean(self):
        warnings.warn('State.clean() is being deprecated, use State.reset().') 
        self.reset()
        self.setup = NIL
        self._questions = list()
        self.teardown = NIL
        self.output = {NIL: ''}

    @cached_property
    def question(self):
        # TODO: Test
        return getattr(thread_storage, 'question', None)

    @property
    def questions(self):
        yield from self._questions

    def add_question(self, name, body):
        self._questions.append(
            Question(
                name=name if name != NIL else len(self._questions),
                body=body,
            )
        )

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
