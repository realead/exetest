import inspect

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


def unit_test_prototype(x, exe, data):#x=>self
    res, msg = ex.execute(exe, data)
    x.assertTrue(res, msg="Wrong test with message: "+msg)

def to_unit_tests(cls):
    for name, value in inspect.getmembers(cls):
        if name.startswith(__DATA_PREFIX):
             method_name=find_unused_name(mangle_name(name), dir(cls))
             setattr(cls, method_name, lambda self, exe=cls.exe, data=value: unit_test_prototype(self, exe, data))
    return cls
