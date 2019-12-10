from typing import Union


class Question:
    def __init__(self, name: Union[str, int], body: tuple, value=0):
        self.name = name
        self.body = body
        self.value = value
        self.results = None
        return

    def __eq__(self, other: 'Question') -> bool:
        return all((self.name == other.name, self.body == other.body))

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'{self.name}: [{self.body}]'