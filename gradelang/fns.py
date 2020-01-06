import os

from .state import state

def award(points: int) -> None:
    state.question.award(points)

def print(string, arguments) -> None:
    # TODO: Lock stdout, print, return
    raise NotImplementedError

def _assert(condition) -> None:
    if not condition:
        raise AssertionError()

def require(*paths) -> None:
    assert all(os.path.exists(p) for p in paths)
