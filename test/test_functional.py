from unittest import TestCase

from gradelang import interpreter
from .samples import *


class TestFunctional(TestCase):

    def test_empty(self):
        interpreter.interpret(Program.empty)
        self.assertListEqual(interpreter.state.setup, [('nil',)])
        return

    def test_setup_failure(self):
        """ Nothing should pass. """
        interpreter.interpret(Program.setup_failure)
        return

    def test_proposal(self):
        interpreter.interpret(Program.proposal)
        return
