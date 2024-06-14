# file_unittest

## Introduction
This package enables the creation and execution of unit tests based on text-based files, also known as _golden testing_. Its primary function is to facilitate the generation of text files (_golden files_) that are regenerated and compared against whenever there are changes in the codebase.

## Installation
Install this package using `pip` by executing the following commands in any active conda environment:

```bash
cd file_unittest/
pip install .
```

## file_unittest.TestCase
Derived from `unittest.TestCase`, this class allows file-based unit testing. Users confirm the correctness of output data by writing to files and verifying that subsequent outputs remain unchanged despite codebase modifications.

## Usage
Instead of inheriting from `unittest.TestCase`, extend `file_unittest.TestCase` and define test functions prefixed with `test_`. For example:

```python
import unittest
import file_unittest

class MyTest(file_unittest.TestCase):
    def test_case(self):
        self.output("hello")

if __name__ == '__main__':
    unittest.main()
```

This approach eliminates the need for explicit assertions like `self.assertTrue` or `self.assertFalse`. The class handles discrepancies in output internally.

### Default Output Location
Output files are stored in the following directory structure:

```
{derived_class_filepath}/test_results/
  {derived_class_filename}.{derived_class_name}.{test_name}.txt
```

### Handling Differences
If the expected output file is missing or differences are detected, the output is saved with a `.new` postfix. The user must verify these `.new` files and, if correct, rename them to `.txt` to serve as new benchmarks.

## Committing Test Results
Once the output `.txt` files meet expectations, commit them to your version control system to establish baselines for future tests.

## Precision Control
Due to potential minor discrepancies caused by code changes (like operation order modifications), it's advisable to control output precision when generating files:

```python
for i in range(len(midpoint_dates)):
    self.output(f'{midpoint_dates[i]:.6f}, {optWs[i]:.6e}, {residuals[i]:.6e}')
```

## Output Display Control
To prevent test results from displaying on the screen, adjust the `setUp()` method:

```python
class MyTest(file_unittest.TestCase):
    def setUp(self):
        self.print_to_screen = False
```

