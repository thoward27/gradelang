from typing import Union


class Question:
    def __init__(self, name: Union[str, int], body: tuple, value=0):
        self.name = name
        self.body = body
        self.value = value
        self.results = None
        self.output = None
        self.exception = None
        return

    def __eq__(self, other: 'Question') -> bool:
        return all((self.name == other.name, self.body == other.body))

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return f'{self.name}: [{self.body}]'

    def report(self):
        base = f'Question {self.name}: {self.score}/{self.max_score}.'
        if self.exception:
            '\n'.join([base, f'Exception thrown: {self.exception}'])
        if self.output:
            '\n'.join([base, f'Output: {self.output}'])
        return base

    def json(self):
        pass

    def markdown(self):
        pass

    def award(self, points):
        self.value += points

    @property
    def score(self):
        return self.value

    @property
    def max_score(self):

        def find(node) -> int:
            if node[0] == 'award':
                return int(node[1])
            elif node[0] == 'seq':
                return find(node[1]) + find(node[2])
            else:
                return 0

        return find(self.body)
