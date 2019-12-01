import unittest
from unittest import TestCase

from gradelang import interpreter
from .samples import *


class TestFunctional(TestCase):

    def test_empty(self):
        interpreter.interpret(Program.empty)
        self.assertEqual(('nil',), interpreter.state.setup)
        return

    def test_setup_failure(self):
        """ Nothing should pass. """
        interpreter.interpret(Program.setup_failure)
        return

    @unittest.skip  # TODO
    def test_proposal(self):
        interpreter.interpret(Program.proposal)
        return
