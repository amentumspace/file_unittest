import unittest
import pathlib
import os
import filecmp
import inspect

class TestCase(unittest.TestCase):

    def hijack(self, func):
        def wrapper():            
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
            result = func()
            # close the output file
            self.outfile.close()
            
            # ensure the new file  was generated
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
        self.outfile.write(msg+'\n')
        if self.print_to_screen:
            print(msg)

    def __init__(self, methodName='runTest', print_to_screen=False):
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
        test_funcs = [f for f in dir(self) if f.startswith('test_')]
        for f in test_funcs:
            # get a pointer to the test function
            fn = getattr(self, f)
            # rewire the function call to execute the
            # wrapped function instead
            setattr(self, f, self.hijack(fn))
        
        # initialise base class
        super().__init__(methodName)
