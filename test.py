import unittest
from assign import *

class TestCases(unittest.TestCase) :
    def testingIntercept(self):
        line = Line((2,2), (5,5))
        line2 = Line((4,2), (4,8))
        self.assertTupleEqual(intersept(line, line2), (4,4))
        #print(str(intersept(line, line2)))
if __name__ == '__main__':
    unittest.main()