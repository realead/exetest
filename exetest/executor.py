import subprocess

from parnames import OPTIONS, EXIT_CODE, STDOUT, STDERR, INPUT

        
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



def check_and_fix_params(params):
    """ inserting default values if none given"""
    if OPTIONS not in params:
        params[OPTIONS]=[]
    
    if INPUT not in params:
        params[INPUT]=""

    


def execute(exe, params):
    """ executes and compares results with expected values.

       if params[EXIT_CODE] not set, the exit code of the process will not be checked
       the same goes for STDOUT and STDERR parameters
    """

    #run test:
    check_and_fix_params(params)
    received=execute_process([exe]+params[OPTIONS], params[INPUT])

    #check results:
    if (EXIT_CODE in params) and (received.exit_code != params[EXIT_CODE]):
        return (False, "Wrong return code! Expected: {0} but received {1}".format(params[EXIT_CODE], received.exit_code))

    if (STDOUT in params) and (received.stdout != params[STDOUT]):
        return (False, "Wrong stdout output! Expected: [{0}] but received [{1}]".format(params[STDOUT], received.stdout))

    if (STDERR in params) and (received.stderr != params[STDERR]):
        return (False, "Wrong stderr output! Expected: [{0}] but received [{1}]".format(params[STDERR], received.stderr))

    return (True, "") 





