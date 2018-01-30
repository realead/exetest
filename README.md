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

#### Tests

Run `sh run_unit_tests.sh` with the virtual environment activated to run all unit tests.
  
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

#### Custom Checkers

It is possible to add custom checkers, there are multiple reasons why they are needed:

   1. Theresults must be compared with some tolerance (e.g. doubles)
   2. More than one result is correct
   3. Part of the results is written on the disc

It is possible do do without custom checkers and use some wrapper for the program to be tested, but custom checkers may be a more convient approach.

We can replace the default checker by overwriting `ex.CHECKERS` which is a list of checkers, for example:
    
    ....
    from exetest.checkers import DoubleChecker

 
    @dec.to_unit_tests
    class TutorialTester:
    ...
       casedata_double_checker={ ex.EXIT_CODE: 0, 
                              ex.INPUT: "1.0", 
                              ex.STDOUT: ".9", 
                              ex.CHECKERS: [DoubleChecker(rel_tolerance=.1, abs_tolerance=.1)]}

Here we use the predefined `DoubleChecker` - the DefaultChecker would fail because the outputs are different, but the `DoubleChecker` accepts this difference.

The checkers must be a callable with signature `xxx(expected, received)` (consult `executor.py` for more details).

If we would like to have a checker in addition to the `DefaultChecker`, we could use `ex.ADDITIONAL_CHECKERS`-option:

 
    class VersionChecker():
        def __init__(self, minversion):
            self.minversion=minversion

        def __call__(self, expected, received):
            if ex.__version__>=self.minversion:
               return True,""
            return False,"exetest too old" 

    @dec.to_unit_tests
    class TutorialTester:
    ...
       casedata_add_checker={ ex.EXIT_CODE: 0, 
                              ex.INPUT: "1.0", 
                              ex.STDOUT: "1.0\n", 
                              ex.ADDITIONAL_CHECKERS: [VersionChecker((0,2,0))]}

Here, the test of the version will be done in addition to the usual `DefaultChecker` and is equivalent to

    from exetest.checkers import DefaultChecker
    ...
      casedata_overwrite_checker={ ex.EXIT_CODE: 0, 
                              ex.INPUT: "1.0", 
                              ex.STDOUT: "1.0\n", 
                              ex.CHECKERS: [DefaultChecker(), VersionChecker((0,2,0))]}

Please take into account, that `DefaultChecker` will be the first checker executed.

It is also possible to use for example a `lambda` as checker, if it suites you:

    casedata_add_lambda={ ex.EXIT_CODE: 0, 
                              ex.INPUT: "1.0", 
                              ex.STDOUT: "1.0\n", 
                              ex.ADDITIONAL_CHECKERS: [lambda expected, received: (True,"") if ex.__version__>=(0,2,0) else (False,"exetest is too old")]}


#### Preparers and Cleaners

There are also hooks to run code prior to the start of the executable and to run code after everything is done for cleaning up. They can be used for example for evaluating files written to the disc.

For this the parameter-keys `ex.PREPARERS` and `ex.CLEANERS` can be used.

The preparers are callable with signature `xxx(parameters)` so they know the starting parameters. If everything worked as expected preparers should return `None` or an empty string or an error-message otherwise. One or more preparers can be defined, for example:

    casedata_preparers={ ex.EXIT_CODE: 0, 
                              ex.INPUT: "1.0", 
                              ex.STDOUT: "1.0\n", 
                              ex.PREPARERS: [lambda pars : None , lambda pars : ""]}

Similar for cleaners - the only difference is that they must have the signature `xxx(parameters, received)` so they know the starting parameters and the returned values:

    casedata_cleaners={ ex.EXIT_CODE: 0, 
                              ex.INPUT: "1.0", 
                              ex.STDOUT: "1.0\n", 
                              ex.CLEANERS: [lambda pars, rec : None , lambda pars, rec : ""]}

#### Input/Output/Errors from files

It is also possible to use text-files as input, output and error:

    import exetest.decorator as dec
    import exetest as ex

    @dec.to_unit_tests
    class FromFileTester:
        exe="python"
        default_parameters = {ex.OPTIONS: ["echoprog.py"],
                              ex.EXIT_CODE: 0}

        casedata_all_from_files={ex.INPUT_FILE:  "input.txt", 
                                 ex.STDERR_FILE: "error.txt",
                                 ex.STDOUT_FILE: "output.txt"}


specifying `ex.XXX_FILE` overwrites the corresponding `ex.XXX`-parameter if it is set, i.e.

        casedata_all_from_files={ex.INPUT_FILE:  "input.txt",    #<==    counts
                                 ex.INPUT: "AAA"}                #doesn't count

#### Discovering test cases from a folder

It is also possible to create test cases automatically from the existing test-case sets in a folder. Let's assume the following structure of the `test_data`-folder:

    test_data
         |----- A.in
         |----- A.out
         |----- A.err
         |----- B.in
         |----- B.out
         |----- C.in

To create test cases A and B we can do the following:

    import exetest as ex
    import exetest.decorator as dec
    import exetest.ts_discovery as ds
       
    @dec.to_unit_tests
    @ds.datasets_from_path("test_data")
    class TestFromPathTester:
        exe="python"
        default_parameters = {ex.OPTIONS: ["echoprog.py"],
                              ex.EXIT_CODE: 0}


The usage of the decorator 

    def datasets_from_path(path, endings=dict(DEFAULT_ENDINGS), needed_files=set(DEFAULT_NEEDED_FILES)):

translates it roughly to the following code:

    @dec.to_unit_tests
    @ds.datasets_from_path("test_data")
    class TestFromPathTester:
        exe="python"
        default_parameters = {ex.OPTIONS: ["echoprog.py"],
                              ex.EXIT_CODE: 0}

        casedata_A={ex.INPUT_FILE:  "testdata/A.in", 
                    ex.STDERR_FILE: "testdata/A.out",
                    ex.STDOUT_FILE: "testdata/A.err"}

        casedata_B={ex.INPUT_FILE:  "testdata/B.in", 
                    ex.STDERR_FILE: "testdata/B.out"}

The role of the files is fixed through the ending of the file and can be customized via `endings`-argument of the decorator, which has the following default:

    DEFAULT_ENDINGS ={ex.INPUT_FILE :  ".in", 
                      ex.STDOUT_FILE : ".out", 
                      ex.STDERR_FILE : ".err"}


As default, a test case is registered if both input and output file with the same name are present. This behavior can be customized via `needed_files`-argument of the decorator. The default is:

    DEFAULT_NEEDED_FILES = set([ex.INPUT_FILE, ex.STDOUT_FILE]) 


## History:

   **0.1.0**: First release

   **0.2.0**: Custom Checker added // Preparers and Cleaners added

   **0.3.0**: Input/Ouput/Error from files // Discovering test cases from a folder

## Future:
 
   1. maximal execution time for a test case
   2. an interface for test runner, so this framework can be used without unittest
   3. other test frameworks as possible targets
   4. python3


                              
             
