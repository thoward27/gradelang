from unittest import TestCase

from gradelang import interpreter
from .samples import *


class TestFunctional(TestCase):

    def test_empty(self):
        interpreter.interpret(Program.empty)
        self.assertListEqual(interpreter.state.setup, [('nil',)])
        return

    def test_setup_failure(self):
        """ Nothing should pass. """
        prog = """
        setup {
            assert 0 > 1;
        } 
        question worth 10 {
            assert 1 > 0;
        }
        """
        interpreter.interpret(prog)
        return

    def test_proposal(self):
        prog = """
        setup {
            Program prog = "echo";
        }

        teardown {}

        save {
            json('results');
            markdown('results');
        }

        question 1 worth 10 points {
            # Run the program, saving output.
            output = prog('hello world');

            # Now let's run some checks.
            assert output exited successfully;
            
            # This checks both stdout and stderr
            assert 'hello' in output;
        }

        question 2 worth 20 points {
            output = prog('hello world');
            assert 'goodbye' not in output;
            award 10 points;
            assert 'hello' in output.stdout;
        }

        question 3 worth 50 points {
            let x be a string;
            assume len(x) >= 1;
            output = prog(x);

            # If we want to just look at stdout.
            assert output.stdout === x;
        }
        """
        interpreter.interpret(prog)
        return
