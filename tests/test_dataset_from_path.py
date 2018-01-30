import inspect

import exetest.decorator as dec
import exetest as ex
import exetest.ts_discovery as ds


def count_test_cases(cls):
   res=0
   for name, value in inspect.getmembers(cls):
        if name.startswith(dec.__TEST_PREFIX):
            res+=1
   return res
    
@dec.to_unit_tests
@ds.datasets_from_path("test_data/echoprog")
class TestFromPathTester:
    exe="python"
    default_parameters = {ex.OPTIONS: ["echoprog.py"],
                          ex.EXIT_CODE: 0}
    def test_count_tests(self):
        self.assertEquals(count_test_cases(self.__class__), 3)


@dec.to_unit_tests
@ds.datasets_from_path("test_data/echoprog", needed_files=set([ex.INPUT_FILE]))
class TestFromPathWithNeededTester:
    exe="python"
    default_parameters = {ex.OPTIONS: ["echoprog.py"],
                          ex.EXIT_CODE: 0}
    def test_count_tests(self):
        self.assertEquals(count_test_cases(self.__class__), 4)


my_endings={ex.INPUT_FILE :  ".my_in",  
            ex.STDOUT_FILE : ".my_out", 
            ex.STDERR_FILE : ".my_err"}


@dec.to_unit_tests
@ds.datasets_from_path("test_data/echoprog", endings=my_endings)
class TestFromPathWithEndingsTester:
    exe="python"
    default_parameters = {ex.OPTIONS: ["echoprog.py"],
                          ex.EXIT_CODE: 0}

    def test_count_tests(self):
        self.assertEquals(count_test_cases(self.__class__), 2)

