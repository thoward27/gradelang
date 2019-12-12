""" Testing Samples.
"""


class Setup:
    """ Setup Snippets.
    """
    empty = "setup {}"
    trivial_passing = "setup { assert 1 == 1; }"
    trivial_failing = "setup { assert 1 == 0; }"
    required_files = 'setup { assert "./README.md" exists }'
    # TODO: This should be moved to a global setup.
    run = 'setup { run "echo", "Hello world"; }'
    touch = 'setup { touch "./temp.txt"; }'


class Question:
    """ Question Snippets.
    # TODO: Reintegrate assume.
    """
    empty = "question {}"
    trivial_passing = "question { assert 1 == 1; }"
    trivial_failing = "question { assert 0 == 1; }"
    testing_output = """
    question {
        run "echo hello world";
        assert "hello world" in stdout;
    }
    """
    awarding_points = """
    question { 
        assert 1 == 1;
        award 10;
    }
    """
    testing_exit_success = """
    question {
        run "echo hello world";
        assert exit successful;
    }
    """
    name_string = 'question "named" {}'
    name_int = 'question 1 {}'
    string_generation = """
    question {
        let x be String(minlen=10, maxlen=100);
        run "echo", x;
        assert x in stdout;
        award 10;
    }
    """


class Teardown:
    """ Teardown Snippets.

    TODO: What does it mean when teardown fails? (Perhaps still 0 credit?)
    """
    empty = "teardown {}"
    trivial_passing = "teardown { assert 1 == 1; }"
    trivial_failing = "teardown { assert 0 == 1; }"
    file_cleanup = 'teardown { remove "./temp.txt"; }'


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
        Question.awarding_points,
        Teardown.empty,
        Output.empty
    ])

    output_json = '\n'.join([
        Setup.trivial_passing,
        Question.trivial_passing,
        Question.trivial_failing,
        Question.awarding_points,
        Teardown.empty,
        Output.json
    ])

    proposal = """
        setup {
            touch "temp.txt";
            run "echo";
            assert exit successful;
        }

        teardown {
            remove "temp.txt";
        }

        output {
            json;
        }

        output {
        }
            question 1 {
            # Run the program, saving output.
            run "echo", "hello world";

            # Now let's run some checks.
            assert exit successful;

            # This checks both stdout and stderr
            assert "hello" in stdout;

            award 10;
        }

        question 2  {
            run "echo", "hello world";
            assert "goodbye" not in stdout;
            award 10;
            assert "hello" in stdout;
            assert "hello" not in stderr;
            award 10;
        }

        question 3 {
            let x be Float(minvalue=1);
            run "echo", x;

            # If we want to just look at stdout.
            assert x in stdout;
            
            String y = "fish";
            run "echo", y;
            assert "fish" in stdout;
            
            let z be String();
            run "echo", z;
            assert z in stdout;
            
            let camel be Int(min_value=6);
            run "echo", camel;
            assert camel in stdout;
            
            award 50;
        }
        """
        
    proposal_questions = """
        setup {
        }

        teardown {
        }

        output {
        }
        
        question 1 {
            # Run the program, saving output.
            run "echo", "hello world";

            # Now let's run some checks.
            assert exit successful;

            # This checks both stdout and stderr
            assert "hello" in stdout;

            award 10;
        }

        question 2  {
            run "echo", "hello world";
            assert "goodbye" not in stdout;
            award 10;
            assert "hello" in stdout;
            assert "hello" not in stderr;
            award 10;
        }

        question 3 {
            let x be Float(minvalue=1);
            run "echo", x;

            # If we want to just look at stdout.
            assert x in stdout;
            
            String y = "fish";
            run "echo", y;
            assert "fish" in stdout;
            
            let z be String();
            run "echo", z;
            assert z in stdout;
            
            let camel be Int(min_value=6);
            run "echo", camel;
            assert camel in stdout;
            
            award 50;
        }
    """
