import sys
sys.path.append("..")


import unittest
from tests.testBloc import *
from tests.testMinage import *
from tests.testTransaction import *

if __name__ == '__main__':
    unittest.main(verbosity=2)