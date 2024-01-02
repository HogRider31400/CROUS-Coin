import sys
sys.path.append("..")
from Transaction import Transaction
from Signature import Signature
##import unittest

tabI = [{montant:50,sigAcheteur:(56,47),cleAcheteur:(1,2)}]
tabO = [{vendeur:"Bob",montant:30,sigVendeur:(34,78),cleVendeur:(3,4)}]
paiementAB = Transaction(tabI,tabO, "Alice")
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