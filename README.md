# file_unittest

## file_unittest.TestCase

This class extends the *unittest.TestCase* class to allow the user to
run unit tests by writing data to a file and verifying the output
has not changed since the last time the unit test was run.

This method is useful if the only benchmark numbers are coming from our
models themselves. 

Once the user is satisfied that the output data is
correct, these unit test simply ensure that the data does not change with
changes in the code base.

### Usage:

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
    {derived_class_path}.{derived_class_name}.{test_name}.txt
```

### Missing or different results:
If the expected output file is missing, or differences are detected,
the output data will be written to the same file, but with .new postfix:

```
        {derived_class_path}.{derived_class_name}.{test_name}.new
```    

- On the first run, the user will need to inspect the .new file for expected
results. 
    
- Otherwise, if differences are detected, the user can diff the 
.txt and .new files to investigate and resolve any differences.

- In both cases once the user is satified with the results, the .new files can 
be renamed with .txt  extension and the .txt files can be checked into the git repo
