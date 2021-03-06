import unittest

from exetest.executor import execute
import exetest as ex

 
 
class ExecutorTester(unittest.TestCase):  

    def test_pwd(self):
        res, mes =  execute("pwd", {ex.STDERR: "", ex.EXIT_CODE: 0})
        self.assertEqual(res, True)
        self.assertEqual(mes, "")
        
    def test_errorcode(self):
        res, mes =  execute("python", {ex.OPTIONS: ["mockprog.py"], ex.STDERR: "", ex.STDOUT: "", ex.EXIT_CODE: 42})
        self.assertEqual(mes, "") 
        self.assertEqual(res, True)

    def test_mockprog1(self):
        res, mes =  execute("python", {ex.OPTIONS: ["mockprog.py", "42"], ex.STDERR: "4242\n", ex.STDOUT: "42\n", ex.EXIT_CODE: 0})
        self.assertEqual(mes, "") 
        self.assertEqual(res, True)

    def test_mockprog2(self):
        res, mes =  execute("python", {ex.OPTIONS: ["mockprog.py", "24"], ex.STDERR: "2424\n", ex.STDOUT: "24\n", ex.EXIT_CODE: 0})
        self.assertEqual(mes, "") 
        self.assertTrue(res)

    def test_exitcode(self):
        res, mes =  execute("python", {ex.OPTIONS: ["mockprog.py", "24"], ex.EXIT_CODE: 1})
        self.assertEqual(mes, "Wrong return code! Expected: 1 but received 0") 
        self.assertEqual(res, False)

    def test_stdout(self):
        res, mes =  execute("python", {ex.OPTIONS: ["mockprog.py", "24"], ex.STDOUT: "nono"})
        self.assertEqual(mes, "Wrong stdout output! Expected: [nono] but received [24\n]") 
        self.assertEqual(res, False)

    def test_stderr(self):
        res, mes =  execute("python", {ex.OPTIONS: ["mockprog.py", "24"], ex.STDERR: "nono"})
        self.assertEqual(mes, "Wrong stderr output! Expected: [nono] but received [2424\n]") 
        self.assertEqual(res, False)

#test input

    def test_emptyinput(self):
        res, mes =  execute("python", {ex.OPTIONS: ["echoprog.py"], ex.STDERR: "", ex.STDOUT: "", ex.EXIT_CODE: 42})
        self.assertEqual(mes, "") 
        self.assertEqual(res, True)

    def test_input1(self):
        res, mes =  execute("python", {ex.OPTIONS: ["echoprog.py"], ex.STDERR: "inputinput\n", ex.STDOUT: "input\n", ex.EXIT_CODE: 0, ex.INPUT: "input"})
        self.assertEqual(mes, "") 
        self.assertEqual(res, True)


    def test_input2(self):
        res, mes =  execute("python", {ex.OPTIONS: ["echoprog.py"], ex.STDERR: "my_inputmy_input\n", ex.STDOUT: "my_input\n", ex.EXIT_CODE: 0, ex.INPUT: "my_input"})
        self.assertEqual(mes, "") 
        self.assertEqual(res, True)


    def test_with_default_parameters(self):
        res, mes =  execute("python", {}, {ex.OPTIONS: ["echoprog.py"], ex.STDERR: "my_inputmy_input\n", ex.STDOUT: "my_input\n", ex.EXIT_CODE: 0, ex.INPUT: "my_input"})
        self.assertEqual(mes, "") 
        self.assertEqual(res, True)

    def test_with_default_parameters_not_overwritten(self):
        res, mes =  execute("python", {ex.EXIT_CODE: 0}, {ex.OPTIONS: ["echoprog.py"], ex.STDERR: "my_inputmy_input\n", ex.STDOUT: "my_input\n", ex.EXIT_CODE: 22, ex.INPUT: "my_input"})
        self.assertEqual(mes, "") 
        self.assertEqual(res, True)


class PreparerCallRecorder:
    def __init__(self):
        self.cnt=0
    def __call__(self, params):
        self.cnt+=1
        self.params=dict(params) 

 

class PreparerTester(unittest.TestCase):  
    def test_call_ones(self):
        rec = PreparerCallRecorder()
        res, mes =  execute("python", {ex.OPTIONS: ["mockprog.py", "24"], ex.EXIT_CODE: 0, ex.PREPARERS: [rec]})
        self.assertEqual(mes, "") 
        self.assertEqual(res, True)
        self.assertEqual(rec.cnt, 1)
        self.assertEqual(rec.params[ex.EXIT_CODE], 0)

    def test_call_twice(self):
        rec = PreparerCallRecorder()
        res, mes =  execute("python", {ex.OPTIONS: ["mockprog.py", "24"], ex.EXIT_CODE: 0, ex.PREPARERS: [rec, rec]})
        self.assertEqual(mes, "") 
        self.assertEqual(res, True)
        self.assertEqual(rec.cnt, 2)
        self.assertEqual(rec.params[ex.EXIT_CODE], 0)

    def test_error_in_preparer(self):
        res, mes =  execute("python", {ex.OPTIONS: ["mockprog.py", "24"], ex.EXIT_CODE: 0, ex.PREPARERS: [lambda a : "Error"]})
        self.assertEqual(mes, "Error") 
        self.assertEqual(res, False)

    def test_return_empty_in_preparer(self):
        res, mes =  execute("python", {ex.OPTIONS: ["mockprog.py", "24"], ex.EXIT_CODE: 0, ex.PREPARERS: [lambda a : ""]})
        self.assertEqual(mes, "") 
        self.assertEqual(res, True)

    def test_return_empty_in_preparer(self):
        res, mes =  execute("python", {ex.OPTIONS: ["mockprog.py", "24"], ex.EXIT_CODE: 0, ex.PREPARERS: [lambda a : None]})
        self.assertEqual(mes, "") 
        self.assertEqual(res, True)



class CleanerCallRecorder:
    def __init__(self):
        self.cnt=0
    def __call__(self, params, received):
        self.cnt+=1
        self.params=dict(params) 
        self.received=received


class CleanerTester(unittest.TestCase):  
    def test_call_ones(self):
        rec = CleanerCallRecorder()
        res, mes =  execute("python", {ex.OPTIONS: ["mockprog.py", "24"], ex.EXIT_CODE: 0, ex.CLEANERS: [rec]})
        self.assertEqual(mes, "") 
        self.assertEqual(res, True)
        self.assertEqual(rec.cnt, 1)
        self.assertEqual(rec.params[ex.EXIT_CODE], 0)
        self.assertEqual(rec.received.exit_code, 0)

    def test_call_twice(self):
        rec = CleanerCallRecorder()
        res, mes =  execute("python", {ex.OPTIONS: ["mockprog.py", "24"], ex.EXIT_CODE: 0, ex.CLEANERS: [rec, rec]})
        self.assertEqual(mes, "") 
        self.assertEqual(res, True)
        self.assertEqual(rec.cnt, 2)
        self.assertEqual(rec.params[ex.EXIT_CODE], 0)
        self.assertEqual(rec.received.exit_code, 0)

    def test_error_in_cleaner(self):
        res, mes =  execute("python", {ex.OPTIONS: ["mockprog.py", "24"], ex.EXIT_CODE: 0, ex.CLEANERS: [lambda a,b : "Error"]})
        self.assertEqual(mes, "Error") 
        self.assertEqual(res, False)

    def test_return_empty_in_cleaner(self):
        res, mes =  execute("python", {ex.OPTIONS: ["mockprog.py", "24"], ex.EXIT_CODE: 0, ex.CLEANERS: [lambda a,b : ""]})
        self.assertEqual(mes, "") 
        self.assertEqual(res, True)

    def test_return_empty_in_cleaner(self):
        res, mes =  execute("python", {ex.OPTIONS: ["mockprog.py", "24"], ex.EXIT_CODE: 0, ex.CLEANERS: [lambda a,b : None]})
        self.assertEqual(mes, "") 
        self.assertEqual(res, True)

    def test_run_cleaner_error_in_preparer(self):
        rec = CleanerCallRecorder()
        res, mes =  execute("python", {ex.OPTIONS: ["mockprog.py", "24"], ex.EXIT_CODE: 0, ex.PREPARERS: [lambda a : "Error"], ex.CLEANERS: [rec, rec]})
        self.assertEqual(mes, "Error") 
        self.assertEqual(res, False)
        self.assertEqual(rec.cnt, 2)
        self.assertEqual(rec.params[ex.EXIT_CODE], 0)
        self.assertEqual(rec.received, None)

    def test_run_cleaner_wrong_answer(self):
        rec = CleanerCallRecorder()
        res, mes =  execute("python", {ex.OPTIONS: ["mockprog.py", "24"], ex.EXIT_CODE: 42, ex.CLEANERS: [rec, rec]})
        self.assertEqual(mes, "Wrong return code! Expected: 42 but received 0") 
        self.assertEqual(res, False)
        self.assertEqual(rec.cnt, 2)
        self.assertEqual(rec.params[ex.EXIT_CODE], 42)
        self.assertEqual(rec.received.exit_code, 0)

    def test_run_cleaner_after_exception(self):
        rec = CleanerCallRecorder()
        with self.assertRaises(Exception) as content:
              execute("python", {ex.OPTIONS: ["mockprog.py", "24"], ex.EXIT_CODE: 0,  ex.PREPARERS: [lambda a : 1/0], ex.CLEANERS: [rec, rec]})
        self.assertEqual(rec.cnt, 2)
        self.assertEqual(rec.params[ex.EXIT_CODE], 0)
        self.assertEqual(rec.received, None)




