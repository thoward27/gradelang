import unittest

from gradelang.interpreter import interpret


class Test(unittest.TestCase):

    def test_setup_empty(self):
        interpret("""
        setup {}
        """)
        return

    def test_setup_prog(self):
        interpret("""
        setup {
            Program prog = "echo";
        }
        """)
        return

    def test_teardown(self):
        interpret("""
        teardown {}
        """)
        return

    def test_question_trivial(self):
        interpret("""
        question 1 worth 1 {
            assert 1 > 0;
        }
        """)
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
