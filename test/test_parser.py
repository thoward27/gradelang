import unittest

from gradelang import parser
from gradelang.state import state
from test.samples import *


class TestSetup(unittest.TestCase):
    def setUp(self) -> None:
        state.reset()
        return

    def test_empty(self):
        parser.parse(Setup.empty)
        self.assertEqual(('nil',), state.setup)
        return

    def test_trivial_failing(self):
        parser.parse(Setup.trivial_failing)
        self.assertEqual(
            ('seq', ('assert', ('==', ('integer', 1), ('integer', 0))), ('nil',)),
            state.setup
        )
        return

    def test_trivial_passing(self):
        parser.parse(Setup.trivial_passing)
        self.assertEqual(
            ('seq', ('assert', ('==', ('integer', 1), ('integer', 1))), ('nil',)),
            state.setup
        )
        return

    def test_echo(self):
        parser.parse(Setup.echo)
        self.assertEqual(
            ('seq', ('assign', 'Program', 'prog', ('string', 'echo')), ('nil',)),
            state.setup
        )
        return


class TestQuestion(unittest.TestCase):
    def setUp(self) -> None:
        state.reset()
        return

    def test_empty(self):
        parser.parse(Question.empty)
        self.assertListEqual(
            [('nil',)],
            state.questions,
        )
        return

    def test_trivial_passing(self):
        parser.parse(Question.trivial_passing)
        self.assertListEqual(
            [('seq', ('assert', ('==', ('integer', 1), ('integer', 1))), ('nil',))],
            state.questions,
        )
        return

    def test_trivial_failing(self):
        parser.parse(Question.trivial_failing)
        self.assertListEqual(
            [('seq', ('assert', ('==', ('integer', 0), ('integer', 1))), ('nil',))],
            state.questions,
        )
        return


class TestSave(unittest.TestCase):
    def test_empty(self):
        parser.parse(Save.empty)
        self.assertEqual(
            ('nil',),
            state.save
        )
        return


class TestProgram(unittest.TestCase):
    def test_empty(self):
        parser.parse(Program.empty)
        self.assertEqual(
            ('nil',),
            state.setup
        )
        self.assertListEqual(
            [('nil',)],
            state.questions
        )
        self.assertEqual(
            ('nil',),
            state.teardown
        )
        self.assertEqual(
            ('nil',),
            state.save
        )
        return

    def test_proposal(self):
        parser.parse(Program.proposal)
        return


class TestStatements(unittest.TestCase):
    def test_comments(self):
        parser.parse("# Comment")
        return

    def test_assignment(self):
        parser.parse('setup { Program p = "echo"; }')
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
