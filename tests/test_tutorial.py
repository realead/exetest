

import exetest.decorator as dec
import exetest as ex
from exetest.checkers import DoubleChecker, DefaultChecker

class VersionChecker():
    def __init__(self, minversion):
        self.minversion=minversion

    def __call__(self, expected, received):
        if ex.__version__>=self.minversion:
           return True,""
        return False,"exetest too old"
         


@dec.to_unit_tests
class TutorialTester:
    exe="python"
    default_parameters = {ex.OPTIONS: ["echoprog.py"],
                          ex.EXIT_CODE: 42,                   
                          ex.INPUT: ""}

    casedata_no_input={}

    casedata_no_input2={ex.STDERR: "", 
                        ex.STDOUT: ""}


    casedata_real_input={ ex.EXIT_CODE: 0, 
                     ex.STDERR: "my_inputmy_input\n", 
                     ex.STDOUT: "my_input\n",  
                     ex.INPUT: "my_input"}

    casedata_double_checker={ ex.EXIT_CODE: 0, 
                              ex.INPUT: "1.0", 
                              ex.STDOUT: ".9", 
                              ex.CHECKERS: [DoubleChecker(rel_tolerance=.1, abs_tolerance=.1)]}

    casedata_add_lambda={ ex.EXIT_CODE: 0, 
                              ex.INPUT: "1.0", 
                              ex.STDOUT: "1.0\n", 
                              ex.ADDITIONAL_CHECKERS: [lambda expected, received: (True,"") if ex.__version__>=(0,2,0) else (False,"exetest is too old")]}
 
    casedata_add_checker={ ex.EXIT_CODE: 0, 
                              ex.INPUT: "1.0", 
                              ex.STDOUT: "1.0\n", 
                              ex.ADDITIONAL_CHECKERS: [VersionChecker((0,2,0))]}

    casedata_overwrite_checker={ ex.EXIT_CODE: 0, 
                              ex.INPUT: "1.0", 
                              ex.STDOUT: "1.0\n", 
                              ex.CHECKERS: [DefaultChecker(), VersionChecker((0,2,0))]}


    casedata_preparers={ ex.EXIT_CODE: 0, 
                              ex.INPUT: "1.0", 
                              ex.STDOUT: "1.0\n", 
                              ex.PREPARERS: [lambda pars : None , lambda pars : ""]}


    casedata_cleaners={ ex.EXIT_CODE: 0, 
                              ex.INPUT: "1.0", 
                              ex.STDOUT: "1.0\n", 
                              ex.CLEANERS: [lambda pars, rec : None , lambda pars, rec : ""]}
  
