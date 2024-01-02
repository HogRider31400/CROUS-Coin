import sys
sys.path.append("../.")


from Transaction import Transaction
import unittest

class testTransaction(unittest.TestCase):

    def setUp(self):
        pass

    def testParseTx(self):
        
        newTx = Transaction.from_text("")

    def testValidTx(self):
        newTx = Transaction.from_text("")

        self.assertFalse(newTx.get_signature() == newTx.signature)

        #faire au moins un cas où c'est vrai