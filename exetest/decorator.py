import inspect
import unittest

import executor as ex

#finds a name not in dictionary:
#checks for name, name1, name2, name3 and so on
def find_unused_name(name, all_names):
   cand=name
   try_cnt=0
   while cand in all_names:
        try_cnt+=1
        cand=name+str(try_cnt)
   return cand



__DATA_PREFIX="casedata_"
__TEST_PREFIX="test_"


def mangle_name(dataname):
    return __TEST_PREFIX+dataname[len(__DATA_PREFIX):]


def unit_test_prototype(x, exe, data, defaults):#x=>self
    res, msg = ex.execute(exe, data, defaults)
    x.assertTrue(res, msg="Wrong test with message: "+msg)

def to_unit_tests(cls):
    #add unittest.TestCase as parent class if needed:
    if unittest.TestCase not in cls.__bases__:
        class new_cls(unittest.TestCase, cls):
            pass
        new_cls.__name__ = cls.__name__
        new_cls.__module__ = cls.__module__
        cls = new_cls


    #extract default parameters:
    defaults={}
    try:
        defaults=cls.default_parameters
    except:
        pass
		
    #add test_XXX methods:
    for name, value in inspect.getmembers(cls):
        if name.startswith(__DATA_PREFIX):
             method_name=find_unused_name(mangle_name(name), dir(cls))
             setattr(cls, method_name, lambda self, exe=cls.exe, data=value, defs=defaults: unit_test_prototype(self, exe, data, defs))
    return cls


