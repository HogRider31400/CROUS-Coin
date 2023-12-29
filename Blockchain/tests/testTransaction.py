import sys
sys.path.append("../.")


from Transaction import Transaction
import unittest

class testTransaction(unittest.TestCase):

    def setUp(self):
        pass

    def testParseTx(self):
        
        newTx = Transaction.from_text(" : A -> B = 10 (27/12/2023-20:03) SIG=(1,2,3,4)")

        self.assertTrue(newTx.id_user_giving == "A")
        self.assertTrue(newTx.id_user_getting =="B")
        self.assertTrue(newTx.amount == "10")
        self.assertTrue(newTx.date == "27/12/2023-20:03")
        self.assertTrue(newTx.signature ==(1,2,3,4))
        self.assertTrue(newTx.previous_block_hash =="")

        newTx = Transaction.from_text(": A -> B = 10 (27/12/2023-20:03) SIG=(1,2,3,4)")
        self.assertTrue(newTx.previous_block_hash =="")

        newTx = Transaction.from_text("BLOB: pedrolito -> poto en verre = 10 (27/12/2023-20:03) SIG=(1,2,3,4)")
        self.assertTrue(newTx.previous_block_hash == "BLOB")
        self.assertTrue(newTx.id_user_giving == "pedrolito")
        self.assertTrue(newTx.id_user_getting == "potoenverre") #pour bien marquer le fait que les espaces c pas dingue, on peut potentiellement les accepter mais dans ce cas faut faire gaffe à mon avis
    
    def testValidTx(self):
        newTx = Transaction.from_text(" : A -> B = 10 (27/12/2023-20:03) SIG=(1,2,3,4)")

        self.assertFalse(newTx.get_signature() == newTx.signature)

        #faire au moins un cas où c'est vrai