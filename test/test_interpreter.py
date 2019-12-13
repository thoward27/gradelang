import json
import os
import unittest
from tempfile import TemporaryDirectory

from gradelang.interpreter import *
from .samples import *


class TestSetup(unittest.TestCase):

    def test_empty(self):
        """ Ensure default value of setup. """
        interpret('\n'.join([Setup.empty, Question.trivial_passing]))
        return

    def test_trivial_passing(self):
        """ Ensure that a simple setup is saved to state. """
        interpret('\n'.join([Setup.trivial_passing, Question.trivial_passing]))
        return

    def test_trivial_failing(self):
        interpret('\n'.join([Setup.trivial_failing, Question.trivial_passing]))
        self.assertTrue(state.setup)
        self.assertNotEqual((), state.setup)
        return

    def test_required_files(self):
        interpret('\n'.join([Setup.required_files_exist, Question.awarding_points]))
        self.assertGreater(state.score(), 0)
        return

    def test_required_files_missing(self):
        interpret('\n'.join([Setup.required_files_missing, Question.awarding_points]))
        self.assertEqual(state.score(), 0)
        return

    def test_run(self):
        interpret('\n'.join([Setup.run, Question.trivial_passing]))
        return

    def test_touch(self):
        with TemporaryDirectory() as fd:
            # Prevent accidental collisions
            path = os.path.join(fd, 'temp.txt')

            # This shouldn't do anything, since there's no question to execute.
            interpret(f'setup {{ touch "{path}"; }}')
            self.assertFalse(os.path.exists(path))

            # Now, this should create the file.
            interpret('\n'.join([f'setup {{ touch "{path}"; }}', Question.trivial_passing]))
            self.assertTrue(os.path.exists(path))
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

    def test_program_exit_specific(self):
        interpret("""
        question {
            run "echo", "hello world";
            assert exit 0;
        }
        """)
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

    def test_file_cleanup(self):
        # This should fail.
        interpret(Teardown.file_cleanup)
        with TemporaryDirectory() as tempdir:
            with open(os.path.join(tempdir, 'temp.txt'), 'w') as fp:
                fp.write('')
            # Now, it should pass.
            interpret(Teardown.file_cleanup)
        return


class TestOutput(unittest.TestCase):
    def test_none(self):
        interpret("")
        self.assertEqual(
            {('nil',): ''},
            state.output
        )
        return

    def test_empty(self):
        interpret('\n'.join([Output.empty, Question.trivial_passing]))
        self.assertEqual(
            {('nil',): ''},
            state.output
        )
        return

    def test_json(self):
        interpret('\n'.join([Output.json, Question.trivial_passing]))
        self.assertEqual(
            {'json': ('nil',)},
            state.output
        )
        return

    def test_markdown(self):
        interpret('\n'.join([Output.markdown, Question.trivial_passing]))
        self.assertEqual(
            {'markdown': ('nil',)},
            state.output
        )
        return

    def test_multiple(self):
        interpret("""
        output { 
            json;
            markdown;
        }
        question {}
        """)
        self.assertEqual(
            {'markdown': ('nil',), 'json': ('nil',)},
            state.output
        )
        return

    def test_filenames(self):
        with TemporaryDirectory() as d:
            path = os.path.join(d, 'results.json')
            interpret("""
            output {
                json "%s";
            }
            question {}
            """ % path)
            self.assertEqual(
                {'json': path},
                state.output
            )
            # Ensure that the json does, in-fact, load back up successfully.
            with open(path, 'r') as f:
                result = json.load(f)
                self.assertIsInstance(result, dict)
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
        self.assertTrue(all(q.exception is not None for q in state.questions))
        return

    def test_proposal(self):
        interpret(Program.proposal)
        return

    def test_proposal_questions(self):
        interpret(Program.proposal_questions)
        return

    def test_output_json(self):
        interpret(Program.output_json)
        return