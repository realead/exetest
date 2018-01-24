import subprocess
import itertools

from parnames import OPTIONS, EXIT_CODE, STDOUT, STDERR, INPUT, CHECKERS, ADDITIONAL_CHECKERS, PREPARERS, CLEANERS, INPUT_FILE, STDOUT_FILE, STDERR_FILE
from checkers import DefaultChecker


def slurp_file(file_name):
    with open(file_name, 'r') as content_file:
        return content_file.read()
        
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
        if INPUT_FILE in params:
            params[INPUT]=slurp_file(params[INPUT_FILE])
        else:
            params[INPUT]=""

    if STDOUT not in params and STDOUT_FILE in params:
        params[STDOUT]=slurp_file(params[STDOUT_FILE])

    if STDERR not in params and STDERR_FILE in params:
        params[STDERR]=slurp_file(params[STDERR_FILE])

    if CHECKERS  not in params:
        params[CHECKERS]=[DefaultChecker()]

    if ADDITIONAL_CHECKERS not in params:
        params[ADDITIONAL_CHECKERS]=[]
    

    
def execute_worker(exe, params, default_params):
        #prepare test:
        for prep in params.get(PREPARERS, []):
            msg=prep(params)
            if msg:
               return False, msg, None

        #run test:
        check_and_fix_params(params, default_params)
        received=execute_process([exe]+params[OPTIONS], params[INPUT])

        #check results:
        for checker in itertools.chain(params[CHECKERS], params[ADDITIONAL_CHECKERS]):
            res, msg = checker(params, received)
            if not res:
                 return res, msg, received

        return True, "", received


def execute(exe, params, default_params={}):
    """ executes and compares results with expected values.

       if params[EXIT_CODE] not set, the exit code of the process will not be checked
       the same goes for STDOUT and STDERR parameters
    """
    
    try:
       res,msg,received = execute_worker(exe, params, default_params)
    except Exception as error:
        #clean up because of error
        for cleaner in params.get(CLEANERS, []):
            msg=cleaner(params, None)
        raise # just let the others handle it...
        
    #clean-up test (normal mode)
    for cleaner in params.get(CLEANERS, []):
        tmp_msg=cleaner(params, received)
        if tmp_msg:
            return False, tmp_msg
    
    return res, msg





