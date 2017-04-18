import unittest

import sys
sys.path.append('..')#exetest

from exetest.executor import execute
import exetest as ex

 
 
class ExecutorTester(unittest.TestCase):  

    def test_pwd(self):
        res, mes =  execute("pwd", {ex.STDERR: "", ex.EXIT_CODE: 0})
        self.assertEquals(res, True)
        self.assertEquals(mes, "")
        
    def test_errorcode(self):
        res, mes =  execute("python", {ex.OPTIONS: ["mockprog.py"], ex.STDERR: "", ex.STDOUT: "", ex.EXIT_CODE: 42})
        self.assertEquals(mes, "") 
        self.assertEquals(res, True)

    def test_mockprog1(self):
        res, mes =  execute("python", {ex.OPTIONS: ["mockprog.py", "42"], ex.STDERR: "4242\n", ex.STDOUT: "42\n", ex.EXIT_CODE: 0})
        self.assertEquals(mes, "") 
        self.assertEquals(res, True)

    def test_mockprog2(self):
        res, mes =  execute("python", {ex.OPTIONS: ["mockprog.py", "24"], ex.STDERR: "2424\n", ex.STDOUT: "24\n", ex.EXIT_CODE: 0})
        self.assertEquals(mes, "") 
        self.assertTrue(res)

    def test_exitcode(self):
        res, mes =  execute("python", {ex.OPTIONS: ["mockprog.py", "24"], ex.EXIT_CODE: 1})
        self.assertEquals(mes, "Wrong return code! Expected: 1 but received 0") 
        self.assertEquals(res, False)

    def test_stdout(self):
        res, mes =  execute("python", {ex.OPTIONS: ["mockprog.py", "24"], ex.STDOUT: "nono"})
        self.assertEquals(mes, "Wrong stdout output! Expected: [nono] but received [24\n]") 
        self.assertEquals(res, False)

    def test_stderr(self):
        res, mes =  execute("python", {ex.OPTIONS: ["mockprog.py", "24"], ex.STDERR: "nono"})
        self.assertEquals(mes, "Wrong stderr output! Expected: [nono] but received [2424\n]") 
        self.assertEquals(res, False)

#test input

    def test_emptyinput(self):
        res, mes =  execute("python", {ex.OPTIONS: ["echoprog.py"], ex.STDERR: "", ex.STDOUT: "", ex.EXIT_CODE: 42})
        self.assertEquals(mes, "") 
        self.assertEquals(res, True)

    def test_input1(self):
        res, mes =  execute("python", {ex.OPTIONS: ["echoprog.py"], ex.STDERR: "inputinput\n", ex.STDOUT: "input\n", ex.EXIT_CODE: 0, ex.INPUT: "input"})
        self.assertEquals(mes, "") 
        self.assertEquals(res, True)


    def test_input2(self):
        res, mes =  execute("python", {ex.OPTIONS: ["echoprog.py"], ex.STDERR: "my_inputmy_input\n", ex.STDOUT: "my_input\n", ex.EXIT_CODE: 0, ex.INPUT: "my_input"})
        self.assertEquals(mes, "") 
        self.assertEquals(res, True)

