Welcome to Gradelang's documentation!
=====================================

.. toctree::
    :maxdepth: 2
    :caption: Contents:
    :glob:
    :hidden:

    pages/*

Introduction
========================

Gradelang is a new domain-specific language designed to alleviate many of the common pains in autograding.

Gradelang allows users to create arbitrarily complex testing conditions for executable files without being locked into
creating Python :code:`TestCase`s relying on :code:`Subprocess.run()`.
Driven by :code:`question` blocks, wrapped with optional :code:`setup` and :code:`teardown` blocks, each question
is executed separately, within it's own process, with results recombined into a final report.

Example
=======================

.. code-block:: none

    setup {
        # @/ represents a special thread-safe location,
        # which is automatically cleaned up when a
        # question exits, successfully or otherwise.
        touch "@/temp.txt";
        run "echo";
        assert exit successful;
    }

    teardown {
        # This is explicit cleanup.
        remove "@/temp.txt";
    }

    output {
        # Output formats with no filename are written to stdout.
        json;
        # Whereas, parameterized formats are written to disk.
        markdown "results.md";
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
