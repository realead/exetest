
from exetest.parnames import OPTIONS, EXIT_CODE, STDOUT, STDERR, INPUT

class CheckerError(Exception):
    def __init__(self, message):
      self.message=message


#default checker,         
class DefaultChecker:
    ##hooks which can be overwritten by subclasses: raise a CheckerError if test not successful
    def check_output(self, expected, received):
        if expected != received:
            raise CheckerError("Wrong stdout output! Expected: [{0}] but received [{1}]".format(expected, received))

    def check_exit_code(self, expected, received): 
        if expected!=received:
           raise CheckerError("Wrong return code! Expected: {0} but received {1}".format(expected, received))

    def check_err_output(self, expected, received):
        if expected!=received:
           raise CheckerError("Wrong stderr output! Expected: [{0}] but received [{1}]".format(expected, received))
        
    def __call__(self, params, received):
        try:
            if (STDOUT in params):
               self.check_output(params[STDOUT], received.stdout)
            if (EXIT_CODE in params):
               self.check_exit_code(params[EXIT_CODE], received.exit_code)
            if (STDERR in params):
               self.check_err_output(params[STDERR], received.stderr)
        except CheckerError as err:
             return (False, err.message)
        return (True, "")
            


class DoubleChecker(DefaultChecker):
    def __init__(self, rel_tolerance=0.0, abs_tolerance=0.0):
        self.rel_tolerance=rel_tolerance
        self.abs_tolerance=abs_tolerance


    def check_output(self, expected, received):
        try:
           r=float(received)
        except:
           raise CheckerError("Received value ["+received+"] isn't a float value")
        try:
           e=float(expected)
        except:
           raise CheckerError("Expected value ["+expected+"] isn't a float value")
        diff=abs(e-r)
        if diff<=self.abs_tolerance:
            return
        val=max(abs(e), abs(r))
        if diff<=self.rel_tolerance*val:
            return
        raise CheckerError("Wrong stdout output! Expected: [{0}] but received [{1}], with difference {2}, which is more than tolerated (rel_tol={3}, abs_tol={4})".format(expected, received, diff, self.rel_tolerance, self.abs_tolerance))
        




