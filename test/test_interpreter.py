import unittest

from gradelang.interpreter import interpret, state
from .samples import *


class TestSetup(unittest.TestCase):

    def test_setup_empty(self):
        """ Ensure default value of setup. """
        interpret(Setup.empty)
        self.assertEqual(state.setup, ('nil',))
        return

    def test_setup_trivial(self):
        """ Ensure that a simple setup is saved to state. """
        interpret(Setup.trivial_passing)
        self.assertEqual(
            ('seq', ('assert', ('==', ('integer', 1), ('integer', 1))), ('nil',)),
            state.setup
        )
        return

    def test_setup_prog(self):
        interpret(Setup.echo)
        self.assertEqual(
            ('seq', ('assign', 'Program', 'prog', ('string', 'echo')), ('nil',)),
            state.setup
        )
        return

    def test_teardown_empty(self):
        interpret(Teardown.empty)
        return

    def test_question_empty(self):
        interpret(Question.empty)
        return

    def test_question_trivial(self):
        interpret(Question.trivial_passing)
        return

    def test_question_program_exit_successful(self):
        interpret(Question.testing_exit_success)
        return

    def test_question_program_output(self):
        interpret(Question.testing_output)
        return
