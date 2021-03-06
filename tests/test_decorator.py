import unittest

import exetest.decorator as dec
import exetest as ex

 
class FindUnusedNameTester(unittest.TestCase):  

    def test_find_in_empty(self):
        self.assertEqual(dec.find_unused_name("name", {}), "name")
        
    def test_find_if_not_yet_in_the_set(self):
        self.assertEqual(dec.find_unused_name("name", ["name_", "name ", "nname"]), "name")
        
    def test_find_1(self):
        self.assertEqual(dec.find_unused_name("name", ["name"]), "name1")
        
    def test_find_2(self):
        self.assertEqual(dec.find_unused_name("name", ["name", "name1"]), "name2")
        
    def test_find_3(self):
        self.assertEqual(dec.find_unused_name("name", ["name", "name1", "name2", "name33", "name4"]), "name3")


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
        self.assertEqual(a.test_input1(), 42) #old method
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

    def test_base_class_preexisted(self):
        @dec.to_unit_tests
        class A(unittest.TestCase):
            def runTest(self):#needed in __init__
                pass

        a=A();#no throw
    
        self.assertEqual(len(A.__bases__), 1)
        self.assertTrue(unittest.TestCase in A.__bases__)


    def test_base_no_class_preexisted(self):
        @dec.to_unit_tests
        class A:
            def runTest(self): #needed in __init__
                pass

        a=A();#no throw
    
        self.assertEqual(len(A.__bases__), 2)
        self.assertTrue(unittest.TestCase in A.__bases__)


    def test_base_other_parent_preexisted(self):      
        class B: pass
        @dec.to_unit_tests
        class A(B):
            def runTest(self): #needed in __init__
                pass

        a=A()#no throw
        self.assertEqual(len(A.__bases__), 2)
        self.assertTrue(unittest.TestCase in A.__bases__)


    def test_base_two_classes(self):      

        @dec.to_unit_tests
        class A:
            def runTest(self): #needed in __init__
                pass
            def ret1(self):
                return 1

        @dec.to_unit_tests
        class B:
            def runTest(self): #needed in __init__
                pass
            def ret2(self):
                return 2

        a=A()#no throw
        b=B()#no throw
        self.assertEqual(a.ret1(), 1)
        self.assertEqual(b.ret2(), 2)

## using decorators:

@dec.to_unit_tests
class OnlyDataBaseClassTester:
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

    def test_self(self):
        #methods were created:
        self.assertTrue(hasattr(self, "test_input1"))
        self.assertTrue(hasattr(self, "test_input2"))    

@dec.to_unit_tests
class AdditionalTester(unittest.TestCase):
    exe="python"
    casedata_xxx1={ex.OPTIONS: ["echoprog.py"], 
                     ex.STDERR: "inputinput\n", 
                     ex.STDOUT: "input\n", 
                     ex.EXIT_CODE: 0, 
                     ex.INPUT: "input"}

    casedata_xxx2={ex.OPTIONS: ["echoprog.py"], 
                     ex.STDERR: "my_inputmy_input\n", 
                     ex.STDOUT: "my_input\n", 
                     ex.EXIT_CODE: 0, 
                     ex.INPUT: "my_input"}

    def test_self(self):
        #methods were created:
        self.assertTrue(hasattr(self, "test_xxx1"))
        self.assertTrue(hasattr(self, "test_xxx2")) 
        self.assertFalse(hasattr(self, "test_input1"))
        self.assertFalse(hasattr(self, "test_input2")) 


@dec.to_unit_tests
class DefaultParametersClassTester:
    exe="python"
    default_parameters = {ex.OPTIONS: ["echoprog.py"], ex.EXIT_CODE: 0}

    casedata_input1={ex.STDERR: "inputinput\n", 
                     ex.STDOUT: "input\n",                    
                     ex.INPUT: "input"}

    casedata_input2={ex.STDERR: "my_inputmy_input\n", 
                     ex.STDOUT: "my_input\n",  
                     ex.INPUT: "my_input"}

    def test_self(self):
        #methods were created:
        self.assertTrue(hasattr(self, "test_input1"))
        self.assertTrue(hasattr(self, "test_input2"))  


#setUp, TearDown, test_* should be kept by the decorator
@dec.to_unit_tests
class KeepOldFunctionalityTester:
    def setUp(self):
        return 10;

    def tearDown(self):
        return 11;

    def test_SetUpExists(self):
        self.assertTrue(hasattr(self, "setUp"))
        self.assertEqual(self.setUp(), 10)

    def test_SetUpExists(self):
        self.assertTrue(hasattr(self, "tearDown")) 
        self.assertEqual(self.tearDown(), 11)


  
