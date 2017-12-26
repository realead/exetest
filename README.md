# exetest

a python framework for testing command line interfaces

## Prerequisites

  1. Python 2.7

## Installation

This is a python2.7 module, to run it/test it you need a python2.7 environment, the easiest way is to use the `virtualenv`:

    virtualenv -p python2.7 p27
    source p27/bin/activate
    (p27)...

To install the module using `pip` run:

    (p27) pip install https://github.com/realead/exetest/zipball/master

It is possible to uninstall it afterwards via
   
    (p27) pip uninstall exetest

You can also install using the `setup.py` file from the root directory of the project:

    (p27)  python setup.py install

However, there is no easy way to deinstall it afterwards (only manually) if `setup.py` was used directly.

You could also use the module without installation, by augmenting the python-path via enviroment variable

    export PYTHONPATH="${PYTHONPATH}:<path_to_exetest>"

or programmatically, for example with help of

    import sys
    sys.path.append(path_to_exetest)


  
## Tutorial

The goal of this framework is to make testing of the command line interfaces as simple as unit testing. 

Let's assume we would like to test the following small python script `echoprog.py`:

    #echoprog.py
    #echo input to stdout and twice to stderr

    import sys

    input_content=sys.stdin.read()

    if not input_content:
        exit(42)

    print input_content
    print >> sys.stderr, input_content*2
    exit(0)

So let's create a first test case, which checks, that the returned code is `42` if there is no input:

    import exetest as ex

    class TutorialTester:
        exe="python"

        casedata_no_input={ex.OPTIONS: ["echoprog.py"],
                           ex.EXIT_CODE: 42,                   
                           ex.INPUT: ""}

Important details are:

  1. the name of the test case data MUST start with `casedata_`.
  2. `exe="python"` defines which executable should be called. There must be a "exe" definition.
  3. `ex.OPTIONS: ["echoprog.py"]` defines the options with which the executable will be started.
  4. `ex.EXIT_CODE: 42` defines the expected exit code. In this case this is 42.
  5. `ex.INPUT: ""` defines the standard input fed to the executable.
  

In the next step we choose the test runner. Right now, the only implemented target is the `unittest`-framework: we save our test set up as `test_tutorial.py` and extend the class with the following decorator:

    import exetest as ex
    import exetest.decorator as dec

    @dec.to_unit_tests
    class TutorialTester:
        ...


Now, run the tests with 
    
    python -m unittest test_tutorial

And we can see, that exact one test has been run successful. Change the expected exit code to see the test fail.

However now we would like to add another test case, which also checks that, if the input is empty, so not only the exit code is `42` but also there was no standard or error output: 

    ...
    @dec.to_unit_tests
    class TutorialTester:
        exe="python"

        casedata_no_input={ex.OPTIONS: ["echoprog.py"],
                           ex.EXIT_CODE: 42,                   
                           ex.INPUT: ""}

        casedata_no_input2={ex.OPTIONS: ["echoprog.py"],
                           ex.EXIT_CODE: 42,                   
                           ex.INPUT: "",
                           ex.STDERR: "", 
                           ex.STDOUT: ""}

Important details are:

  1. `ex.STDERR: ""` defines the expected stander error output, in this case this should be empty.
  2. `ex.STDERR: ""` defines the standard input fed to the executable.
  3. the name of the test case data MUST start with `casedata_`.

After running the unittest framework we can see, that now there are 2 successful tests.

However, we also could factor out the common set up into a variable called `default_parameters` (this name is a must!) for example:

    ...
    @dec.to_unit_tests
    class TutorialTester:
        exe="python"
        default_parameters = {ex.OPTIONS: ["echoprog.py"],
                              ex.EXIT_CODE: 42,                   
                              ex.INPUT: ""}

        casedata_no_input={}

        casedata_no_input2={ex.STDERR: "", 
                            ex.STDOUT: ""}

The default parameters can be easily overwritten in a test case definition:

    ...
    @dec.to_unit_tests
    class TutorialTester:
        exe="python"
        default_parameters = {ex.OPTIONS: ["echoprog.py"],
                              ex.EXIT_CODE: 42,                   
                              ex.INPUT: ""}
        ...
        casedata_real_input={ ex.EXIT_CODE: 0, #<============  HERE! 
                         ex.STDERR: "my_inputmy_input\n", 
                         ex.STDOUT: "my_input\n",  
                         ex.INPUT: "my_input"} #<============  and HERE!


Now there are 3 successful tests!


## Future:
 
   1. maximal execution time for a test case
   2. an interface for test runner, so this framework can be used without unittest
   3. other test frameworks as possible targets
   4. python3


                              
             
