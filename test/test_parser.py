import unittest

from gradelang import parser
from .samples import *


class TestSetup(unittest.TestCase):
    def test_empty(self):
        parser.parse(Setup.empty)
        return

    def test_trivial(self):
        parser.parse(Setup.trivial_failing)
        parser.parse(Setup.trivial_passing)
        return

    def test_echo(self):
        parser.parse(Setup.echo)
        return


class TestQuestion(unittest.TestCase):
    def test_empty(self):
        parser.parse(Question.empty)
        return

    def test_trivial(self):
        parser.parse(Question.trivial_passing)
        parser.parse(Question.trivial_failing)
        return


class TestSave(unittest.TestCase):
    def test_empty(self):
        parser.parse(Save.empty)
        return


class TestProgram(unittest.TestCase):
    def test_empty(self):
        parser.parse(Program.empty)
        return

    def test_proposal(self):
        parser.parse(Program.proposal)
        return


class TestStatements(unittest.TestCase):
    def test_comments(self):
        parser.parse("# Comment")
        return

    def test_assignment(self):
        parser.parse('Program p = "echo";')
        return

    def test_comparisons(self):
        parser.parse('assert 1 == 1;')
        parser.parse('assert 1 >= 1;')
        parser.parse('assert 1 >= 1;')
        parser.parse('assert 0 <= 1;')
        parser.parse('assert 0 < 1;')
        parser.parse('assert 1 >= 0;')
        parser.parse('assert 1 > 0;')
        return
