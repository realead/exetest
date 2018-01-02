import unittest

import exetest as ex
from exetest.executor import execute
from exetest.checkers import DefaultChecker, DoubleChecker


 
 
class CheckerTester(unittest.TestCase):  

    #wrong exit_code, but no checker, so ok...
    def test_no_checkers(self):
        #canary:
        res, mes =  execute("python", {ex.OPTIONS: ["echoprog.py"], ex.EXIT_CODE: 0})
        self.assertEquals(res, False)
        #test:
        res, mes =  execute("python", {ex.OPTIONS: ["echoprog.py"], ex.EXIT_CODE: 0, ex.CHECKERS: []})
        self.assertEquals(mes, "") 
        self.assertEquals(res, True)


    #default checker fails but not double
    def test_checker_overwritten(self):
        params={ex.OPTIONS: ["echoprog.py"], ex.INPUT: "42", ex.EXIT_CODE: 0, ex.STDOUT: "41"}
        #canary:
        res, mes =  execute("python", params)
        self.assertEquals(res, False)
        #test:
        params[ex.CHECKERS]=[DoubleChecker(abs_tolerance=1.1)]
        res, mes =  execute("python", params)
        self.assertEquals(mes, "") 
        self.assertEquals(res, True)


    #last checker fails
    def test_last_checker_used(self):
        params={ex.OPTIONS: ["echoprog.py"], ex.INPUT: "42", ex.EXIT_CODE: 0, ex.STDOUT: "41", ex.CHECKERS: [DoubleChecker(abs_tolerance=1.1)]}
        #canary:
        res, mes =  execute("python", params)
        self.assertEquals(res, True)
        #test:
        params[ex.CHECKERS]=[DoubleChecker(abs_tolerance=1.1), DefaultChecker()]
        res, mes =  execute("python", params)
        self.assertEquals(res, False)

    #first checker fails
    def test_first_checker_used(self):
        params={ex.OPTIONS: ["echoprog.py"], ex.INPUT: "42", ex.EXIT_CODE: 0, ex.STDOUT: "41", ex.CHECKERS: [DoubleChecker(abs_tolerance=1.1)]}
        #canary:
        res, mes =  execute("python", params)
        self.assertEquals(res, True)
        #test:
        params[ex.CHECKERS]=[DefaultChecker(), DoubleChecker(abs_tolerance=1.1)]
        res, mes =  execute("python", params)
        self.assertEquals(res, False)

    def test_additional_checker_used(self):
        params={ex.OPTIONS: ["echoprog.py"], ex.INPUT: "42", ex.EXIT_CODE: 0, ex.STDOUT: "41", ex.CHECKERS: [DoubleChecker(abs_tolerance=1.1)]}
        #canary:
        res, mes =  execute("python", params)
        self.assertEquals(res, True)
        #test:
        params[ex.CHECKERS]=[DoubleChecker(abs_tolerance=1.1)]
        params[ex.ADDITIONAL_CHECKERS]=[DefaultChecker()]
        res, mes =  execute("python", params)
        self.assertEquals(res, False)


    def test_checker_used_first(self):
        double_checker=DoubleChecker(abs_tolerance=0.9)
        params={ex.OPTIONS: ["echoprog.py"], ex.INPUT: "42", ex.EXIT_CODE: 0, ex.STDOUT: "41", ex.CHECKERS: [double_checker]}
        expected_err_msg="Wrong stdout output! Expected: [41] but received [42\n]"#default checker message
        #canary:
        res, msg =  execute("python", params)
        self.assertEquals(res, False)
        self.assertFalse(msg==expected_err_msg)
        #test:
        params[ex.CHECKERS]=[DefaultChecker()]
        params[ex.ADDITIONAL_CHECKERS]=[double_checker]
        res, msg =  execute("python", params)
        self.assertEquals(res, False)
        self.assertEquals(msg,expected_err_msg)



