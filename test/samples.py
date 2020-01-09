""" Testing Samples.
"""


class Statements:
    """ Generic Statements.
    """
    assert_success = 'assert 1 == 1;'
    assert_failure = 'assert 1 == 0;'
    assert_exit_success = 'assert exit success;'
    assert_exit_failure = 'assert exit failure;'
    assert_exit_status5 = 'assert exit 5;'
    assert_exit_statusn = lambda n: f'assert exit {n};'
    assert_in_success = 'assert "A" in "ABC";'
    assert_in_failure = 'assert "A" in "XYZ";'
    assert_not_in_success = 'assert "A" not in "XYZ";'
    assert_not_in_failure = 'assert "A" not in "ABC";'

    award_0 = 'award 0;'
    award_1 = 'award 1;'
    award_n = lambda n: f'award {n}'

    check_success = 'check 1 == 1;'
    check_failure = 'check 1 == 0;'

    declaration_int_success = 'Int x = 0;'
    declaration_int_failure = 'Int x = "A";'
    declaration_int_n = lambda n: f'Int x = {n};'
    declaration_float_success = 'Float x = 0.0;'
    declaration_float_failure = 'Float x = "A";'
    declaration_float_n = lambda n: f'Float x = {n};'
    declaration_str_success = 'String x = "Hello";'
    declaration_str_failure = 'String x = 0;'
    declaration_str_str = lambda s: f'String x = {s};'

    lambda_int_identity = 'Int x = lambda n: n;'
    lambda_int_add_1 = 'Int x: lambda n: n + 1;'
    lambda_float_identity = 'Float x: lambda n: n;'
    lambda_float_div_10 = 'Float x: lambda n: n / 10;'
    lambda_str_identity = 'String x = lambda c: c;'
    lambda_str_concat = 'String x = lambda s1, s2: s1 + s2;'
    
    require_success = 'require "./README.md";'
    require_failure = 'require "Imaginary.files.are.not.real.files.;'
    
    run_success = 'run "echo";'
    run_exception = 'run "python", "-c", "raise Exception";'
    run_echo_hello = 'run "echo", "Hello world";'
    run_cmd_not_found = 'run "notatool", "not an arg";'


class Setup:
    """ Setup Snippets.
    """
    empty = "setup {}"
    trivial_passing = "setup { assert 1 == 1; }"
    trivial_failing = "setup { assert 1 == 0; }"
    required_files_exist = 'setup { require "./README.md"; }'
    required_files_missing = 'setup { require "./not-a-file-no-way-no-how.imaginary"; }'
    # TODO: This should be moved to a global setup.
    run = 'setup { run "echo", "Hello world"; }'
    touch = 'setup { touch "./temp.txt"; }'


class Question:
    """ Question Snippets.
    # TODO: Reintegrate assume.
    """
    empty = "question \"empty\"{}"
    trivial_passing = "question \"trivial_passing\" { assert 1 == 1; }"
    trivial_failing = "question \"trivial_failing\"{ assert 0 == 1; }"
    testing_output = """
    question {
        run "echo hello world";
        assert "hello world" in stdout;
    }
    """
    awarding_points = """
    question \"awarding points\"{ 
        assert 1 == 1;
        award 10;
    }
    """
    testing_exit_success = """
    question \"exit success\"{
        run "echo hello world";
        assert exit successful;
    }
    """
    name_string = 'question "named" {}'
    name_int = 'question 123 {}'
    string_generation = """
    question \"string\"{
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
            touch "@/temp.txt";
            run "echo";
            assert exit successful;
        }

        teardown {
            remove "@/temp.txt";
        }

        output {
            json;
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
            run "printf", z;
            assert z in stdout;
            
            let camel be Int(min_value=6);
            run "echo", camel;
            assert camel in stdout;
            
            award 50;
        }
        """

    proposal_questions = """
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
            let x be Float(minvalue=1.0);
            run "echo", x;

            # If we want to just look at stdout.
            assert x in stdout;
            
            String y = "fish";
            run "echo", y;
            assert "fish" in stdout;
            
            let z be String();
            run "printf", z;
            assert z in stdout;
            
            let camel be Int(min_value=6);
            run "echo", camel;
            assert camel in stdout;
            
            award 50;
        }
    """
