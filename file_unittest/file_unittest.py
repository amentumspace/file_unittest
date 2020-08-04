import unittest
import pathlib
import os
import filecmp
import inspect

class TestCase(unittest.TestCase):
    """
    This class extends the unittest.TestCase class to allow the user to
    run unit tests by writing data to a file and verifying the output
    has not changed since the last time the unit test was run.

    This method is useful if the only benchmark numbers are coming from our
    models themselves. Once the user is satisfied that the output data is
    correct, these unit test simply ensure that the data does not change with
    changes in the code base.

    Usage:
        Rather than inherit from unittest.TestCase the user should
        derive a class from file_unittest.TestCase.

        Like the normal unit test, individual test functions 
        are appended with test_

        Any desired output data is written by calling self.output

        Eg:
        class MyTest(file_unittest.TestCase):
            def test_case(self):
                self.output("hello")

        Unlike the normal unittest.TestCase the user does not need to
        make any calls to eg. self.assertTrue, self.assertFalse etc.

        This class will take care of warning about any differences in output.

    Default output location:
        The default location to output the data will be:
            {derived_class_filepath}/test_results/
                {derived_class_filename}.{derived_class_name}.{test_name}.txt

    Missing or different results:
        If the expected output file is missing, or differences are detected,
        the output data will be written to the same file, but with .new postfix:
            {derived_class_filepath}/test_results/
                {derived_class_filename}.{derived_class_name}.{test_name}.new
        
        - On the first run, the user will need to inspect the .new file for expected
        results. 
        
        - Otherwise, if differences are detected, the user can diff the 
        .txt and .new files to investigate and resolve any differences.

        In both cases, once the user is satified the .new files can be renamed 
        .txt and the .txt files can be checked into the git repo
    """ 

    def hijack(self, func):
        """
        This method wraps our test_ functions 
        (called by the unittest package) through this wrapper code
        which handles file output and comparison.

        Any test errors (differences in txt output files) will be
        raised here. 
        """
        def wrapper():
            ###
            # Dont use docstrings here. They will obfuscate any warning messages
            # from unittest because we are "really" calling func()
            # 
            # Creates a unique output filename and opens a handle to the file
            # for output by the self.output() function below.
            ###
            #             
            # construct the output file name in 
            # the format {module}.{class}.{method}
            func_name = func.__name__
            output_basename = f'{self.module_name}.{self.class_name}.{func_name}'            
            
            # generate the existing (.txt) and newly generated (.new) filenames
            output_new_name = f'{output_basename}.new'
            output_ext_name = f'{output_basename}.txt'

            # get the full paths of the output files
            new_filepath = f"{self.out_filepath}/{output_new_name}"
            ext_filepath = f"{self.out_filepath}/{output_ext_name}"
            
            # create the output folder if it does not exist
            os.makedirs(os.path.dirname(new_filepath), exist_ok=True)
            
            # delete the new file if it already exists
            if os.path.exists(new_filepath):
                os.remove(new_filepath)
            # ensure that the new file does not exist
            self.assertFalse(os.path.exists(new_filepath), 
                            f"Could not delete new file '{new_filepath}'")

            # open the file to be populated by self.output() called by our test function
            self.outfile = open(new_filepath, "w")
            # call the test function            
            func()
            # close the output file
            self.outfile.close()
            
            # ensure the new file was generated
            self.assertTrue(os.path.exists(new_filepath), 
                            f"Could not generate new file '{new_filepath}'")
            
            # warn if the existing, benchmark, file is missing
            self.assertTrue(os.path.exists(ext_filepath), 
                            f"Could not find existing file '{ext_filepath}'")
            
            # check file contents are identical
            self.assertTrue(filecmp.cmp(ext_filepath, new_filepath), 
                            f'\nFiles differ:\n  {ext_filepath}\n  {new_filepath}')
            
            # If we made it this far, all tests passed,
            # so we can delete the .new file
            if os.path.exists(new_filepath):
                os.remove(new_filepath)
        return wrapper
    
    def output(self, msg):
        """
        Write the message to the output file and write to screen if requested
        """
        self.outfile.write(msg+'\n')
        if self.print_to_screen:
            print(msg)
            
    def __init__(self, methodName='runTest', print_to_screen=True):
        """
        Determine the derived class file path name
        and the name of the derived class. These are used to generate
        the output file path.

        It also reroutes all test_ functions through our wrapper code above.
        """
        # whether we output test results to screen
        self.print_to_screen = print_to_screen

        # output files relative to the child class file patth        
        child_filename = inspect.getfile(self.__class__)
        child_filepath = (str)(pathlib.Path(child_filename).parent.absolute())
        self.out_filepath = child_filepath + "/test_results"

        # save the python module containing our child class
        parts = os.path.splitext(child_filename)
        self.module_name = parts[len(parts) - 2]

        # save our child class name
        self.class_name = type(self).__name__

        # hijack the test functions
        test_funcs = [f for f in dir(self) 
                        if f.startswith('test_') and callable(getattr(self,f))]

        for f in test_funcs:
            # get a pointer to the test function
            fn = getattr(self, f)
            # rewire the function call to execute the wrapped function instead
            setattr(self, f, self.hijack(fn))
        
        # initialise base class
        super().__init__(methodName)
