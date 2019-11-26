import unittest

from gradelang import lexer


class TestLexer(unittest.TestCase):
    def test_setup(self):
        lexer.input("""
        setup {
            Program prog = 'echo';
        }
        """)
        self.assertEqual(lexer.token().type, 'SETUP')
        return

    def test_teardown(self):
        lexer.input("""
        teardown {}
        """)
        self.assertEqual(lexer.token().type, 'TEARDOWN')
        return

    def test_save(self):
        lexer.input("""
        save {
            json('results');
        }
        """)
        self.assertEqual(lexer.token().type, 'SAVE')
        return

    def test_question_simple(self):
        lexer.input("""
        question 1 worth 10 {
            assert 1 > 0;
        }
        """)
        self.assertEqual(lexer.token().type, 'QUESTION')
        return

    def test_question_basic(self):
        lexer.input("""
        question 1 worth 10 {
            prog('hello world');
            assert prog exited successfully;
        }
        """)
        self.assertEqual(lexer.token().type, 'QUESTION')
        return

    def test_comments(self):
        lexer.input("""
        # Commenting.
        """)
        self.assertEqual(lexer.token(), None)
        return
