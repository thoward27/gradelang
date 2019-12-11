import unittest

from gradelang import parser
from gradelang.question import Question
from gradelang.state import state
from test import samples


class TestSetup(unittest.TestCase):
    def setUp(self) -> None:
        state.clean()
        return

    def test_empty(self):
        parser.parse(samples.Setup.empty)
        self.assertEqual(('nil',), state.setup)
        return

    def test_trivial_failing(self):
        parser.parse(samples.Setup.trivial_failing)
        self.assertEqual(
            ('seq', ('assert', ('==', ('integer', 1), ('integer', 0))), ('nil',)),
            state.setup
        )
        return

    def test_trivial_passing(self):
        parser.parse(samples.Setup.trivial_passing)
        self.assertEqual(
            ('seq', ('assert', ('==', ('integer', 1), ('integer', 1))), ('nil',)),
            state.setup
        )
        return

    def test_run(self):
        parser.parse(samples.Setup.run)
        # TODO
        return


class TestQuestion(unittest.TestCase):
    def setUp(self) -> None:
        state.clean()
        return

    def test_empty(self):
        parser.parse(samples.Question.empty)
        self.assertListEqual(
            [Question(name=0, body=('nil',))],
            list(state.questions),
        )
        return

    def test_trivial_passing(self):
        parser.parse(samples.Question.trivial_passing)
        self.assertListEqual(
            [Question(name=0, body=('seq', ('assert', ('==', ('integer', 1), ('integer', 1))), ('nil',)))],
            list(state.questions),
        )
        return

    def test_trivial_failing(self):
        parser.parse(samples.Question.trivial_failing)
        self.assertListEqual(
            [Question(name=0, body=('seq', ('assert', ('==', ('integer', 0), ('integer', 1))), ('nil',)))],
            list(state.questions),
        )
        return


class TestSave(unittest.TestCase):
    def test_empty(self):
        parser.parse(samples.Output.empty)
        self.assertEqual(
            [],
            state.output
        )
        return


class TestProgram(unittest.TestCase):
    def setUp(self) -> None:
        state.clean()
        return

    def test_empty(self):
        parser.parse(samples.Program.empty)
        self.assertEqual(
            ('nil',),
            state.setup
        )
        self.assertListEqual(
            [Question(name=0, body=('nil',))],
            list(state.questions)
        )
        self.assertEqual(
            ('nil',),
            state.teardown
        )
        self.assertEqual(
            [],
            state.output
        )
        return

    @unittest.skip
    def test_proposal(self):
        parser.parse(samples.Program.proposal)
        return


class TestStatements(unittest.TestCase):
    def test_comments(self):
        parser.parse("# Comment")
        return

    def test_assignment(self):
        parser.parse('setup { String p = "echo"; }')
        return

    def test_comparisons(self):
        parser.parse('setup { assert 1 == 1;}')
        parser.parse('setup { assert 1 >= 1; }')
        parser.parse('setup { assert 1 >= 1; }')
        parser.parse('setup { assert 0 <= 1; }')
        parser.parse('setup { assert 0 < 1; }')
        parser.parse('setup { assert 1 >= 0; }')
        parser.parse('setup { assert 1 > 0; }')
        return
