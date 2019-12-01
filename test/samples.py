""" Testing Samples.
"""


class Setup:
    """ Setup Snippets.
    """
    empty = "setup {}"
    trivial_passing = "setup { assert 1 == 1; }"
    trivial_failing = "setup { assert 1 == 0; }"
    echo = 'setup { Program prog = "echo"; }'


class Question:
    """ Question Snippets.
    """
    empty = "question {}"
    trivial_passing = "question { assert 1 == 1; }"
    trivial_failing = "question { assert 0 == 1; }"
    testing_output = """
    question {
        run "echo hello world";
        assert exit successful;
        assert "hello world" in stdout;
    }
    """
    testing_exit_success = """
    question {
        Program prog = "echo";
        results = prog("hello world");
        assert results exited successfully;
    }
    """


class Teardown:
    """ Teardown Snippets.

    TODO: What does it mean when teardown fails? (Perhaps still 0 credit?)
    """
    empty = "teardown {}"
    trivial_passing = "teardown { assert 1 == 1; }"
    trivial_failing = "teardown { assert 0 == 1; }"


class Output:
    """ Output Snippets.
    """
    empty = "output {}"
    json = 'output { json; }'
    markdown = 'output { markdown; }'


class Program:
    """ Predefined Programs.
    """
    empty = '\n'.join([
        Setup.empty,
        Question.empty,
        Teardown.empty,
        Output.empty
    ])

    setup_failure = '\n'.join([
        Setup.trivial_failing,
        Question.trivial_passing,
        Teardown.empty,
        Output.empty
    ])

    proposal = """
        setup {
            Program prog = "echo";
        }

        teardown {}

        output {
            json 'results';
            markdown 'results';
        }

        question 1 {
            # Run the program, saving output.
            output = prog('hello world');

            # Now let's run some checks.
            assert output exited successfully;

            # This checks both stdout and stderr
            assert 'hello' in output;

            award 10;
        }

        question 2  {
            output = prog('hello world');
            assert 'goodbye' not in output;
            award 10;
            assert 'hello' in output.stdout;
            award 10;
        }

        question 3 {
            let x be a string;
            assume len(x) >= 1;
            output = prog(x);

            # If we want to just look at stdout.
            assert output.stdout === x;
            award 50 total;
        }
        """
