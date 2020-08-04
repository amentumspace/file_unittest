# file_unittest

## Introduction

This package provides a way to create and run unit tests based on text-based files.

Its purpose is to allow the user to generate a set of text files which
are then re-generated and compared whenever the tested code-base changes. 

## Installation

The preferred installation method is to use `pip install`.

The package can be installed into any active conda environment by running:

```
cd file_unittest/   # cd into this directory
pip install .
```

## file_unittest.TestCase

This class extends the *unittest.TestCase* class to allow the user to
run unit tests by writing data to a file and verifying the output
has not changed since the last time the unit test was run.

This method is useful if the only benchmark numbers are coming from our
models themselves. 

Once the user is satisfied that the output data is
correct, these unit test simply ensure that the data does not change with
changes in the code base.

## Usage:

Rather than inherit from *unittest.TestCase* the user should
derive a class from *file_unittest.TestCase*.

Like the normal unit test, individual test functions 
are appended with *test_*.

Any desired output data is written by calling `self.output`

Example python test file:

```python
import unittest
import file_unittest

class MyTest(file_unittest.TestCase):
    def test_case(self):
        self.output("hello")

if __name__ == '__main__':
    unittest.main()
```

- Unlike the normal *unittest.TestCase* the user does not need to
make any assertion calls eg. `self.assertTrue`, `self.assertFalse` etc.

- This class will take care of warning about any differences in output.

### Default output location:

The default location to output the data will be:

```
    {derived_class_filepath}/test_results/
      {derived_class_filename}.{derived_class_name}.{test_name}.txt
```

### Missing or different results:

If the expected output file is missing, or differences are detected,
the output data will be written to the same file, but with .new postfix:

```
    {derived_class_filepath}/test_results/
      {derived_class_filename}.{derived_class_name}.{test_name}.new
```    

- On the first run, the user will need to inspect the .new file for expected
results;
    
- Otherwise, if differences are detected, the user can diff the 
.txt and .new files to investigate and resolve any differences;

- In both cases once the user is satisfied with the results, the .new files can 
be renamed with .txt  extension and the .txt files can be checked into the git repo

## Committing test result files to source control

Once the output *.txt* files have been satisfactorily generated as in the
previous step, they should be checked into source control so that they
can be used as the benchmark for future runs.

## A note on output precision

This unit test framework does a simple file comparison after the text files
have been generated. 

It will raise an exception if the two files are not identical.

Sometimes code changes will result in small changes in output,
for instance due to changing the order of operations, and some small changes
in output might be acceptable. 

In this case it is recommended to control the precision of the output when generating the files.

For instance, an example test case might be written as follows:

```python
for i in range(len(midpoint_dates)):
    self.output(f'{midpoint_dates[i]:.6f}, {optWs[i]:.6e}, {residuals[i]:.6e}')
```

Here we control the output format (float vs scientific) and precision.

## Controlling output to screen

By default, test results will also be output to screen.

This can be controlled in the setUp() method of the class

```python
class MyTest(file_unittest.TestCase):
    def setUp(self):
        self.print_to_screen = False
```
