import unittest
import file_unittest

class MyFileTest(file_unittest.TestCase):
    
    def test_case(self):
        self.output('bad')

    def test_case2(self):
        self.output('good')

if __name__ == '__main__':
    unittest.main()
