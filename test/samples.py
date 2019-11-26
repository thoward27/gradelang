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
    empty = "question worth 1 {}"
    trivial_passing = "question worth 1 { assert 1 == 1; }"
    trivial_failing = "question worth 1 { assert 0 == 1; }"


class Teardown:
    """ Teardown Snippets.

    TODO: What does it mean when teardown fails? (Perhaps still 0 credit?)
    """
    empty = "teardown {}"
    trivial_passing = "teardown { assert 1 == 1; }"
    trivial_failing = "teardown { assert 0 == 1; }"


class Save:
    """ Save Snippets.

    TODO: Save to JSON
    TODO: Save to Markdown
    """
    empty = "save {}"


class Program:
    """ Predefined Programs.
    """
    empty = '\n'.join([Setup.empty, Question.empty, Teardown.empty, Save.empty])

    proposal = """
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
