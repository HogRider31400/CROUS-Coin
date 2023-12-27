import sys
sys.path.append("..")


from Bloc import Bloc
import unittest

example_block = """
        {
            "previous_block_hash" : "aopziejazeokhazeazeaze",
            "transactions" : [
                " : A -> B = 10 (27/12/2023-20:03) SIG=(1,2,3,4)"
            ],
            "magic_number" : 10
        }
"""
example_block2 = """
        {
            "previous_block_hash" : "aopziejazeokhazeazeaze",
            "transactions" : [
                " : A -> B = 10 (27/12/2023-20:03) SIG=(1,2,3,4)"
            ],
            "magic_number" : null
        }
"""

class testBloc(unittest.TestCase):

    def setUp(self):
        bloc = Bloc.from_text(example_block)
        bloc2 = Bloc.from_text(example_block2)

    def testParseBlock(self):


        self.assertTrue(bloc.previous_block_hash == "aopziejazeokhazeazeaze")
        self.assertTrue(len(bloc.transactions) == 1)
        self.assertTrue(bloc.magic_number == 10)

        self.assertTrue(bloc.magic_number == None)

    def testMinedBloc(self):
        self.assertTrue(bloc.is_mined())
        self.assertFalse(bloc2.is_mined())

    def testValidBloc(self):
        self.assertFalse(bloc.is_valid())
        self.assertFalse(bloc2.is_valid())



