import unittest

from gradelang import lexer


class TestLexer(unittest.TestCase):
    def test_setup(self):
        lexer.input("""
        setup {
            Program prog = 'echo';
        }
        """)
        return

    def test_teardown(self):
        lexer.input("""
        teardown {}
        """)
        return

    def test_save(self):
        lexer.input("""
        save {
            json('results');
        }
        """)
        return

    def test_question_simple(self):
        lexer.input("""
        question 1 worth 10 {
            assert 1 > 0;
        }
        """)
        return

    def test_question_basic(self):
        lexer.input("""
        question 1 worth 10 {
            prog('hello world');
            assert prog exited successfully;
        }
        """)
        return
