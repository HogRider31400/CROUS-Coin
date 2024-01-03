import sys
sys.path.append("..")  
sys.path.append("../EllipticCurves")
from Bloc import Bloc
import unittest

example_block = """
        {
            "previous_block_hash" : "aopziejazeokhazeazeaze",
            "timestamp" : 19783097830983,
            "transactions" : [
                
            ],
            "coinbase_transaction" : null,
            "pow_number" : 10
        }
"""
example_block2 = """
        {
            "previous_block_hash" : "aopziejazeokhazeazeaze",
            "timestamp" : 19783097830984,
            "transactions" : [
                
            ],
            "coinbase_transaction" : null,
            "pow_number" : null
        }
"""

class testBloc(unittest.TestCase):

    def setUp(self):
        self.bloc = Bloc.from_text(example_block)
        self.bloc2 = Bloc.from_text(example_block2)
        

    def testParseBlock(self):


        self.assertTrue(self.bloc.previous_block_hash == "aopziejazeokhazeazeaze")
        self.assertTrue(len(self.bloc.transactions) == 0)
        self.assertTrue(self.bloc.get_pow_number() == 10)
        self.assertTrue(self.bloc2.get_pow_number() == None)

    def testHashBloc(self):
        self.hash1 = self.bloc.get_block_hash()
        print("hash bloc 1: ")
        print(int.from_bytes(self.hash1, 'big'))
        self.assertTrue(self.hash1 == self.bloc.get_block_hash())

    def testMinedBloc(self):
        self.assertTrue(self.bloc.is_mined())
        self.assertFalse(self.bloc2.is_mined())

    def testValidBloc(self):
        """self.assertFalse(bloc.is_valid())
        self.assertFalse(bloc2.is_valid())"""



