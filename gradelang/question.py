from tempfile import TemporaryDirectory
from typing import Union


class Question:
    def __init__(self, name: Union[str, int], body: tuple, value=0):
        self.name = name
        self.body = body
        self.value = value
        self.results = None
        self.output = None
        self.exception = None
        self.traceback = None
        return

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        return

    def __eq__(self, other: 'Question') -> bool:
        return all((self.name == other.name, self.body == other.body))

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return f'{self.name}: [{self.body}]'

    @property
    def workdir(self):
        if '_workdir' not in self.__dict__:
            self.__dict__['_workdir'] = TemporaryDirectory(prefix=f'{self.name}-')
        return self.__dict__['_workdir']

    def report(self):
        base = f'Question {self.name}: {self.score}/{self.max_score}.'
        if self.exception:
            base = '\n'.join([base, f'Exception thrown: {self.exception}\n{self.traceback}'])
        if self.output:
            base = '\n'.join([base, f'Output: {self.output}'])
        return base

    def json(self):
        return {
            'name': self.name,
            'max_score': self.max_score,
            'score': self.score,
            'output': '\n'.join(filter(lambda x: x, [self.output, self.exception, self.traceback]))
        }

    def markdown(self):
        return '\n'.join(filter(lambda x: x, [
            f'### {self.name} {self.score}/{self.max_score}',
            self.output,
            self.exception,
            self.traceback
        ]))

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
