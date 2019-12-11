import os
import unittest

from gradelang.interpreter import *
from .samples import *


class TestSetup(unittest.TestCase):

    def test_setup_empty(self):
        """ Ensure default value of setup. """
        interpret(Setup.empty)
        return

    def test_setup_trivial(self):
        """ Ensure that a simple setup is saved to state. """
        interpret(Setup.trivial_passing)
        return

    def test_setup_required_files(self):
        interpret(Setup.required_files)
        return

    def test_compilation(self):
        interpret(Setup.run)
        return

    def test_create_files(self):
        interpret(Setup.touch)
        self.assertTrue(os.path.exists('temp.txt'))
        return


class TestQuestion(unittest.TestCase):
    def test_question_empty(self):
        interpret(Question.empty)
        return

    def test_question_trivial_passing(self):
        interpret(Question.trivial_passing)
        q = list(state.questions)
        self.assertEqual(len(q), 1)
        q = q[0]
        self.assertEqual(q.score, 0)
        self.assertEqual(q.exception, None)
        return

    def test_question_trivial_failing(self):
        interpret(Question.trivial_failing)
        self.assertEqual(len(list(state.questions)), 1)
        q = list(state.questions)[0]
        self.assertEqual(q.score, 0)
        self.assertNotEqual(q.exception, None)
        return

    def test_question_program_exit_successful(self):
        interpret(Question.testing_exit_success)
        return

    def test_question_program_output(self):
        interpret(Question.testing_output)
        return

    def test_award_points(self):
        interpret(Question.awarding_points)
        return


class TestTeardown(unittest.TestCase):
    def test_teardown_empty(self):
        interpret(Teardown.empty)
        return


class TestProgram(unittest.TestCase):
    pass


class TestOutput(unittest.TestCase):
    pass
