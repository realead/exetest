import os
from exetest.parnames import INPUT_FILE, STDOUT_FILE, STDERR_FILE
from exetest import decorator as dec

DEFAULT_ENDINGS ={INPUT_FILE :  ".in", 
                  STDOUT_FILE : ".out", 
                  STDERR_FILE : ".err"}


DEFAULT_NEEDED_FILES = set([INPUT_FILE, STDOUT_FILE]) 

def stem(file_name):
   return os.path.splitext(os.path.basename(file_name))[0] 

def extension(file_name):  
   return os.path.splitext(file_name)[1] 

def filter_test_cases(files, endings, needed_files):
    tc_names=set([stem(f) for f in files])
    test_cases={tc_name:{} for tc_name in tc_names}
    #group files
    for f in files:
        tc_name=stem(f)
        for key, ending in endings.items():
            if f.endswith(ending):
                test_cases[tc_name][key]=f

    test_cases
    #filter out non-complete  cases
    res = { tc_name : options for tc_name, options in test_cases.items() if needed_files.issubset(options.keys())}
    return res
        
    

def discover_test_cases(dir_path, endings=dict(DEFAULT_ENDINGS), needed_files=set(DEFAULT_NEEDED_FILES)): 
    exts=endings.values()
    files_of_interest=[]
    for f in os.listdir(dir_path):
        if extension(f) in exts:
            files_of_interest.append(os.path.join(dir_path,f))
    return filter_test_cases(files_of_interest, endings, needed_files)

   
### decorator:
def datasets_from_path(path, endings=dict(DEFAULT_ENDINGS), needed_files=set(DEFAULT_NEEDED_FILES)):
    def decorator(cls):
        test_cases=discover_test_cases(path, endings, needed_files)
        for name, options in test_cases.items():
            setattr(cls, dec.__DATA_PREFIX+name, dict(options))
        return cls
    return decorator 

