import subprocess
import itertools

from parnames import OPTIONS, EXIT_CODE, STDOUT, STDERR, INPUT, CHECKERS, ADDITIONAL_CHECKERS, PREPARERS, CLEANERS
from checkers import DefaultChecker

        
class CallResult:
    def __init__(self, out, err, exit_code):
        self.stdout=out
        self.stderr=err
        self.exit_code=exit_code


def execute_process(command, command_input): 
    df = subprocess.Popen(command,  stdin=subprocess.PIPE, stdout=subprocess.PIPE,  stderr=subprocess.PIPE)        
    output, err = df.communicate(input=command_input)
    code=df.returncode
    return CallResult(output, err, code)



def check_and_fix_params(params, default_params):
    """ inserting default values if none given"""
    for key,val in default_params.items():
		if key not in params:
			params[key]=val

    if OPTIONS not in params:
        params[OPTIONS]=[]
    
    if INPUT not in params:
        params[INPUT]=""

    if CHECKERS  not in params:
        params[CHECKERS]=[DefaultChecker()]

    if ADDITIONAL_CHECKERS not in params:
        params[ADDITIONAL_CHECKERS]=[]
    

    


def execute(exe, params, default_params={}):
    """ executes and compares results with expected values.

       if params[EXIT_CODE] not set, the exit code of the process will not be checked
       the same goes for STDOUT and STDERR parameters
    """
    #prepare test:
    for prep in params.get(PREPARERS, []):
        msg=prep(params)
        if msg:
           return False, msg

    #run test:
    check_and_fix_params(params, default_params)
    received=execute_process([exe]+params[OPTIONS], params[INPUT])

    #check results:
    for checker in itertools.chain(params[CHECKERS], params[ADDITIONAL_CHECKERS]):
        res, msg = checker(params, received)
        if not res:
             return (res, msg)

    #clean-up test:
    for cleaner in params.get(CLEANERS, []):
        msg=cleaner(params, received)
        if msg:
            return (False,msg)
    
    return (True, "") 





