import unittest
from unittest import TestCase

from gradelang import interpreter
from .samples import *


class TestFunctional(TestCase):

    def test_empty(self):
        interpreter.interpret(Program.empty)
        self.assertEqual(('nil',), interpreter.state.setup)
        return

    def test_setup_failure(self):
        """ Nothing should pass. """
        interpreter.interpret(Program.setup_failure)
        return
    
    
    def test_propsal_light(self):
        interpreter.interpret("""
        setup {
            String prog = "echo";
        }

        teardown {}

        output {
            json; 
            markdown;
        }

        question 1 {
            # Run the program, saving output.
            run "echo hello world";

            # Now let's run some checks.
            assert exit successful;

            # This checks both stdout and stderr
            assert "hello" in stdout;

            award 10;
        }
        question 2  {
            run "echo hello world";
            assert "world" in stdout;
            award 10;
            assert "hello" in stdout;
            award 10;
        }
        question 3 {
            String x = "fish";
            run "echo x";

            assert x in stdout;
            award 50;
        }

        """)
        return

    @unittest.skip  # TODO
    def test_proposal(self):
        interpreter.interpret(Program.proposal)
        return
