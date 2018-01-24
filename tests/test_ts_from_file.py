import exetest.decorator as dec
import exetest as ex


INPUT_FILE_NAME="test_data/ts_files/input.txt"
OUTPUT_FILE_NAME="test_data/ts_files/output.txt"
ERROR_FILE_NAME="test_data/ts_files/error.txt"


@dec.to_unit_tests
class FromFileTester:
    exe="python"
    default_parameters = {ex.OPTIONS: ["echoprog.py"],
                          ex.EXIT_CODE: 0}


    casedata_input_file={ex.INPUT_FILE: INPUT_FILE_NAME, 
                         ex.STDERR: "my_input\nmy_input\n\n",
                         ex.STDOUT: "my_input\n\n"}


    #input_file trumps input
    casedata_overwritten_input_file={ex.INPUT_FILE: INPUT_FILE_NAME,
                         ex.INPUT: "A", 
                         ex.STDERR: "my_input\nmy_input\n\n",
                         ex.STDOUT: "my_input\n\n"}


    casedata_inout_files={ex.INPUT_FILE: INPUT_FILE_NAME, 
                          ex.STDERR: "my_input\nmy_input\n\n",
                          ex.STDOUT_FILE: OUTPUT_FILE_NAME}


    #ouput_file trumps stdout
    casedata_overwritten_out_file={ex.INPUT_FILE: INPUT_FILE_NAME, 
                          ex.STDOUT: "A\n",
                          ex.STDOUT_FILE: OUTPUT_FILE_NAME}

    casedata_all_files={ex.INPUT_FILE: INPUT_FILE_NAME, 
                          ex.STDERR_FILE: ERROR_FILE_NAME,
                          ex.STDOUT_FILE: OUTPUT_FILE_NAME}


    #stderr_file trumps stderr
    casedata_overwritten_err_file={ex.INPUT_FILE: INPUT_FILE_NAME, 
                          ex.STDERR: "AA\n",
                          ex.STDERR_FILE: ERROR_FILE_NAME}

