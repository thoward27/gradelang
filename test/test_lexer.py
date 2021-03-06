import unittest

from gradelang import lexer
from .samples import *


class TestLexer(unittest.TestCase):
    def test_setup(self):
        lexer.input(Setup.empty)
        self.assertEqual(lexer.token().type, 'SETUP')
        return

    def test_teardown(self):
        lexer.input(Teardown.empty)
        self.assertEqual(lexer.token().type, 'TEARDOWN')
        return

    def test_output(self):
        lexer.input(Output.empty)
        self.assertEqual(lexer.token().type, 'OUTPUT')
        return

    def test_question(self):
        lexer.input(Question.empty)
        self.assertEqual(lexer.token().type, 'QUESTION')
        return

    def test_question_basic(self):
        lexer.input(Question.trivial_passing)
        self.assertEqual(lexer.token().type, 'QUESTION')
        return

    def test_comments(self):
        lexer.input("# Commenting!")
        self.assertEqual(lexer.token(), None)
        return

    def test_strings(self):
        lexer.input(""""String"exit"string 2\"""")
        self.assertEqual(lexer.token().type, 'STRING')
        self.assertEqual(lexer.token().type, 'EXIT')
        self.assertEqual(lexer.token().type, 'STRING')
        return
