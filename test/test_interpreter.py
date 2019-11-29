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
        interpret("""
        question 1 worth 10 {
            Program prog = "echo";
            prog("Hello world");
            assert prog exited successfully;
        }
        """)
        return

    def test_question_program_output(self):
        interpret("""
        question 1 worth 10 {
            Program prog = "echo";
            output = prog("Hello world");
            assert output == "hello world";
        }
        """)
        return
