# gradelang

A DMS for autograding.

## Example

```
setup {
    # Things in this block are executed before each question

    # You can do things like require that files exist
    assert "README.md" exists;

    # You can also compile binaries here
    run "./compile.sh", "target";

    # Run commands take an arbitrary list of strings, which are
    # then executed using subprocess.run()
    
    # Another option is creating any files your scripts may need
    touch "@/temp.txt";
    
    # Within gradelang, @/ represents a special, thread-safe folder.
    # Things created under @/ are only accessible to the currently
    # executing question. Files leftover in @/ are automatically cleaned.
}

teardown {
    # Things in this block are executed after each question
    
    # Since, in this example, we are using thread-safe storage,
    # we don't have to do anything!    
}

output {
    # This block dictates the output format for the results.
    # Each format can optionally take a filename.
    # Results are only written after completion of all questions,
    # therefore, @/ is not defined within this block (nor should it be!)
    json "results.json";
    markdown;
    
    # Running this block will log the results to a json-formatted file
    # named "results.json". Then, it will log the results as markdown
    # to stdout, which is the default value if no filename is given.
}

question {
    # Questions are all run in separate processes behind the scenes.
    # Each question represents a separate block, each should be completely
    # independent, they should not share resources, and they should only
    # use their own thread-safe storage.
    
    # Questions should always begin with a call to Run().
    run "echo", "hello world";
    
    # Then, you can make arbitrary assertions about the results from the
    # call to run.
    assert exit successful;
    
    # The exit keyword checks the return code of the program.
    # You can compare to both successful and failure.
    
    # Gradelang also supports keywords such as in; 
    # which may examine both stdout and stdin.
    assert "hello" in stdout;
    
    # At any point, you may award the student points
    award 10;
    
    # The maximum score for a question is a sum of the award statements.
    # Once an assert fails, the student will not be awarded any further
    # points, and the question exits.
}
# You can make as many questions as you'd like! You can also name them.
question "Meaning of life" {
    assert 1 == 1;
    award 10;
}
```

## Setup

To get started you can install gradelang directly from PyPI.

```
python -m pip install gradelang
```

Once `gradelang` is installed, it can be called directly as a module:

```
python -m gradelang <file.grade>
```

## Key Contributors

Thanks to the efforts of Mary Wishart and Brittany Lewis, for help getting this project off of the ground and shipping v1.
