
from parnames import OPTIONS, EXIT_CODE, STDOUT, STDERR, INPUT


#default checker,         
class DefaultChecker:
    def __call__(self, params, received):
        if (EXIT_CODE in params) and (received.exit_code != params[EXIT_CODE]):
            return (False, "Wrong return code! Expected: {0} but received {1}".format(params[EXIT_CODE], received.exit_code))

        if (STDOUT in params) and (received.stdout != params[STDOUT]):
            return (False, "Wrong stdout output! Expected: [{0}] but received [{1}]".format(params[STDOUT], received.stdout))

        if (STDERR in params) and (received.stderr != params[STDERR]):
            return (False, "Wrong stderr output! Expected: [{0}] but received [{1}]".format(params[STDERR], received.stderr))

        return (True, "") 
            






