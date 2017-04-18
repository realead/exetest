import unittest

import sys
sys.path.append('..')#exetest

import exetest.decorator as dec
import exetest as ex

 
class FindUnusedNameTester(unittest.TestCase):  

    def test_find_in_empty(self):
        self.assertEquals(dec.find_unused_name("name", {}), "name")
        
    def test_find_if_not_yet_in_the_set(self):
        self.assertEquals(dec.find_unused_name("name", ["name_", "name ", "nname"]), "name")
        
    def test_find_1(self):
        self.assertEquals(dec.find_unused_name("name", ["name"]), "name1")
        
    def test_find_2(self):
        self.assertEquals(dec.find_unused_name("name", ["name", "name1"]), "name2")
        
    def test_find_3(self):
        self.assertEquals(dec.find_unused_name("name", ["name", "name1", "name2", "name33", "name4"]), "name3")


class ToUnitTestDecoratorTester(unittest.TestCase):
    def test_one_casedata(self):
        @dec.to_unit_tests
        class A(unittest.TestCase):
            def runTest(self):#needed in __init__
                pass
            exe="python"
            casedata_input1={ex.OPTIONS: ["echoprog.py"], 
                             ex.STDERR: "inputinput\n", 
                             ex.STDOUT: "input\n", 
                             ex.EXIT_CODE: 0, 
                             ex.INPUT: "input"}

        a=A();
        self.assertTrue(hasattr(a, "test_input1"))
        self.assertTrue(a.test_input1() is None) #check no assertion raised


    def test_one_casedata_no_overwrite(self):
        @dec.to_unit_tests
        class A(unittest.TestCase):
            def runTest(self):#needed in __init__
                pass
            exe="python"
            casedata_input1={ex.OPTIONS: ["echoprog.py"], 
                             ex.STDERR: "inputinput\n", 
                             ex.STDOUT: "input\n", 
                             ex.EXIT_CODE: 0, 
                             ex.INPUT: "input"}
            def test_input1(self):
                return 42

        a=A();
        self.assertTrue(hasattr(a, "test_input1"))
        self.assertTrue(hasattr(a, "test_input11"))
        self.assertEquals(a.test_input1(), 42) #old method
        self.assertTrue(a.test_input11() is None) #new method, no throw


    def test_two_casedatas(self):
        @dec.to_unit_tests
        class A(unittest.TestCase):
            def runTest(self):#needed in __init__
                pass
            exe="python"
            casedata_input1={ex.OPTIONS: ["echoprog.py"], 
                             ex.STDERR: "inputinput\n", 
                             ex.STDOUT: "input\n", 
                             ex.EXIT_CODE: 0, 
                             ex.INPUT: "input"}

            casedata_input2={ex.OPTIONS: ["echoprog.py"], 
                             ex.STDERR: "my_inputmy_input\n", 
                             ex.STDOUT: "my_input\n", 
                             ex.EXIT_CODE: 0, 
                             ex.INPUT: "my_input"}

        a=A();
        self.assertTrue(hasattr(a, "test_input1"))
        self.assertTrue(hasattr(a, "test_input2"))
        self.assertTrue(a.test_input1() is None) #no throw
        self.assertTrue(a.test_input2() is None) #no throw

   