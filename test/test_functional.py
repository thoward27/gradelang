from unittest import TestCase

from gradelang import interpreter
from .samples import *


class TestFunctional(TestCase):

    def test_empty(self):
        """ A completely empty program. """
        interpreter.interpret(Program.empty)
        self.assertEqual(('nil',), interpreter.state.setup)
        return

    def test_setup_failure(self):
        """ Nothing should pass. """
        interpreter.interpret(Program.setup_failure)
        self.assertEqual(sum(q.score for q in interpreter.state.questions), 0)
        return

    def test_proposal(self):
        """ The proposal example. """
        interpreter.interpret(Program.proposal)
        return

    def test_proposal_questions(self):
        """ Proposal with just questions. """
        interpreter.interpret(Program.proposal_questions)
        self.assertEqual(80, interpreter.state.score())
        return
