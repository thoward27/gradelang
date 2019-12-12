import os
import unittest

from gradelang.interpreter import *
from .samples import *


class TestSetup(unittest.TestCase):

    def test_empty(self):
        """ Ensure default value of setup. """
        interpret(Setup.empty)
        return

    def test_trivial_passing(self):
        """ Ensure that a simple setup is saved to state. """
        interpret(Setup.trivial_passing)
        return

    def test_trivial_failing(self):
        interpret(Setup.trivial_failing)
        self.assertTrue(state.setup)
        self.assertNotEqual((), state.setup)

    @unittest.skip
    def test_required_files(self):
        interpret(Setup.required_files)
        return

    def test_run(self):
        interpret(Setup.run)
        return

    @unittest.skip
    def test_touch(self):
        interpret(Setup.touch)
        self.assertTrue(os.path.exists('temp.txt'))
        return


class TestQuestion(unittest.TestCase):
    def test_empty(self):
        interpret(Question.empty)
        return

    def test_trivial_passing(self):
        interpret(Question.trivial_passing)
        q = list(state.questions)
        self.assertEqual(len(q), 1)
        q = q[0]
        self.assertEqual(q.score, 0)
        self.assertEqual(q.exception, None)
        return

    def test_trivial_failing(self):
        interpret(Question.trivial_failing)
        self.assertEqual(len(list(state.questions)), 1)
        q = list(state.questions)[0]
        self.assertEqual(q.score, 0)
        self.assertNotEqual(q.exception, None)
        return

    def test_program_exit_successful(self):
        interpret(Question.testing_exit_success)
        return

    def test_program_output(self):
        interpret(Question.testing_output)
        return

    def test_award_points(self):
        interpret(Question.awarding_points)
        self.assertEqual(10, state.score())
        return


class TestTeardown(unittest.TestCase):
    def test_empty(self):
        interpret(Teardown.empty)
        return

    def test_trivial_passing(self):
        interpret(Teardown.trivial_passing)
        return

    def test_trivial_failing(self):
        interpret(Teardown.trivial_failing)
        return

    @unittest.skip
    def test_file_cleanup(self):
        # This should fail.
        interpret(Teardown.file_cleanup)
        # TODO: Use tempfile
        with open('temp.txt', 'w') as f:
            f.write('')
        # Now, it should pass.
        interpret(Teardown.file_cleanup)
        return


class TestOutput(unittest.TestCase):
    def test_empty(self):
        interpret(Output.empty)
        return

    def test_json(self):
        interpret(Output.json)
        return

    def test_markdown(self):
        interpret(Output.markdown)
        return


class TestProgram(unittest.TestCase):
    def test_empty(self):
        interpret(Program.empty)
        self.assertEqual(('nil',), state.setup)
        self.assertEqual(0, state.score())
        self.assertListEqual([], [q.exception for q in state.questions if q.exception])
        return

    def test_setup_failure(self):
        interpret(Program.setup_failure)
        self.assertNotEqual((), state.setup)
        self.assertEqual(0, state.score())
        self.assertTrue(all(isinstance(q.exception, AssertionError) for q in state.questions))
        return

    @unittest.skip
    def test_proposal(self):
        interpret(Program.proposal)
        return

    def test_proposal_questions(self):
        interpret(Program.proposal_questions)
        return
