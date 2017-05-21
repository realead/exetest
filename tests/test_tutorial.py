import sys
sys.path.append('..')#exetest

import exetest.decorator as dec
import exetest as ex


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
 


  
