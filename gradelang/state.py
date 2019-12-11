""" gradelang State.
"""
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
                # TODO: Can we sum all possible points? AKA # of AWARD statements?
                value=0
            )
        )
        return

    def update_results(self, results):
        self.results = results
        if self.output:
            self.writeOutput()
        
    def writeOutput(self):
        import json
        if 'json' in self.output:
            with open("output.json", 'a') as f:
                jsonOutput = json.dumps(self.results.stdout)
                f.write(jsonOutput)
        if 'markdown' in self.output:
            with open("output.md", 'a') as f:
                f.write(self.results.stdout)


state = State()
