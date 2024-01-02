import sys
sys.path.append("..")

from Bloc import Bloc
import unittest

example_block = """
        {
            "previous_block_hash" : "aopziejazeokhazeazeaze",
            "timestamp" : 19783097830983,
            "transactions" : [
                
            ],
            "pow_number" : 10
        }
"""
example_block2 = """
        {
            "previous_block_hash" : "aopziejazeokhazeazeaze",
            "timestamp" : 19783097830984,
            "transactions" : [
                
            ],
            "pow_number" : null
        }
"""

class testBloc(unittest.TestCase):

    def setUp(self):
        bloc = Bloc.from_text(example_block)
        bloc2 = Bloc.from_text(example_block2)

    def testParseBlock(self):


        """self.assertTrue(bloc.previous_block_hash == "aopziejazeokhazeazeaze")
        self.assertTrue(bloc.previous_block_hash == "aopziejazeokhazeazeaze")
        self.assertTrue(len(bloc.transactions) == 1)
        self.assertTrue(bloc.magic_number == 10)

        self.assertTrue(bloc.magic_number == None)"""

    def testMinedBloc(self):
        """self.assertTrue(bloc.is_mined())
        self.assertFalse(bloc2.is_mined())
        self.assertTrue(bloc.is_mined())
        self.assertFalse(bloc2.is_mined())"""

    def testValidBloc(self):
        """self.assertFalse(bloc.is_valid())
        self.assertFalse(bloc2.is_valid())"""



