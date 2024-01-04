import sys
sys.path.append("..")
sys.path.append("../EllipticCurves")

from Minage import Minage
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

class testMinage(unittest.TestCase):

    def setUp(self):
        self.bloc = Bloc.from_text(example_block) 


    



