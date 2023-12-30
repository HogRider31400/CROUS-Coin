from Transaction import Transaction
##import unittest

paiementAB = Transaction('30/12/2023',("Alice31",50,"BobSigne"))
tabT = [("Jacques2",50,"BobSigne2")]
paiementAB.ajouterInputs(tabT)
paiementAB.__repr__()

##class testTransaction(unittest.TestCase):
##
##    def setUp(self):
##        pass
##
##    def testRepr():
##        #Alice et Jacques payent 50 C à Bob
##        paiementAB = Transaction(("Alice31",50,"BobSigne"))
##        paiementAB.ajouterInputs([("Jacques2",50,"BobSigne2")])
##        paiementAB.__repr__()