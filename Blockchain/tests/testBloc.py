import sys
sys.path.append("..")  
sys.path.append("../EllipticCurves")
from Bloc import Bloc
import unittest
import Transaction
from Signature import Signature
from Point import Point
from CourbeElliptique import CourbeElliptique
from utils import courbe
from Utilisateur import Utilisateur

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
            "timestamp" : null,
            "transactions" : [
                
            ],
            "coinbase_transaction" : null,
            "pow_number" : null
        }
"""

'''--50-->Alice--30-->Bob'''
CE = CourbeElliptique(*courbe)
sigAcheteur = Signature(5439102160533729286291568068280253624165601758875954373768139906654721812274359516693644104284664715234766909782804012342090970415733450516337396768657875, 3486100964449987698544044351520014096183120411052438692040586311244810061267024468023696112323354013173659169321654104653757331092616393675757819802075970)
cleAcheteur = Point(3118285745690082516819838297607382631466653731077196052604216247694373586220294590672106850852280689331172015968294762428131521271281940315228083078173564, 10478894441751583738987044209342758263493827312595290610628159206083819451722646942925992412226360091079021427865278944013668768657919161283910205625581649,CE)
sigVendeur = Signature(6239620238231195149935410106005719780248441283951589381887273808500278162300411124053825646994691143222348259078778694483265942818217345172458084101309303, 3915100741136112862853987721242368465758100068649234333395041302415382190493767702954737026378600372852792961824973096328064512786241726473306196095602381)
cleVendeur = Point(8484445204163366193830149330078115049235616364220758419176782190939615781364471782056917011806805156043914601247665778528157581030055621063961460238682051, 3179642056146878138054123425892357801021704685421506102661972210112319209698516560334307705784968320325088423766650553397393695038883968375717204253839574,CE)
tabI = [{"montant":50,"sigAcheteur":sigAcheteur,"cleAcheteur":cleAcheteur}]
tabO = [{"vendeur":"Bob","montant":30,"sigVendeur":sigVendeur,"cleVendeur":cleVendeur}]
        


class testBloc(unittest.TestCase):

    def setUp(self):
        self.bloc = Bloc.from_text(example_block)
        self.bloc2 = Bloc.from_text(example_block2)
        self.paiementAB = Transaction.Transaction(tabI,tabO, "Alice",3456789.232323)
        self.utilisateur = Utilisateur(1)
        

    def testParseBlock(self):


        self.assertTrue(self.bloc.previous_block_hash == "aopziejazeokhazeazeaze")
        self.assertTrue(len(self.bloc.transactions) == 0)
        self.assertTrue(self.bloc.get_pow_number() == 10)
        self.assertTrue(self.bloc2.get_pow_number() == None)

    def testHashBloc(self):
        hash1 = self.bloc.get_block_hash()
        hash2 = self.bloc2.get_block_hash()
        self.assertTrue(hash1 == self.bloc.get_block_hash())
        self.assertTrue(hash2 == -1)
        self.bloc2.set_pow_number(13)
        hash2 = self.bloc2.get_block_hash()
        self.assertTrue(hash2 !=-1)
        self.assertTrue(hash2 != hash1)


    def testMinedBloc(self):
        self.assertFalse(self.bloc2.is_mined())
        #a modifier 
        self.assertTrue(self.bloc2.get_size_target()<3)
        self.bloc2.set_pow_number(23)
        self.assertFalse(self.bloc2.is_mined())
        #ici avec 26 on a deux 0 en début
        self.bloc2.set_pow_number(26)
        self.assertTrue(self.bloc2.is_mined())

    def testValidBloc(self):
        """self.assertFalse(self.bloc.is_valid())
        self.assertFalse(self.bloc2.is_valid())
        self.bloc2.set_pow_number(26)
        self.assertTrue(self.bloc2.is_valid())"""

    def testSetCoinbaseTransaction(self):
        self.assertTrue(self.bloc2.get_coinbase_transaction()==None)
        self.bloc2.set_coinbase_transaction(10, self.utilisateur)
        ct1 = self.bloc2.get_coinbase_transaction()
        self.assertTrue(ct1!=None)
        self.bloc2.set_coinbase_transaction(4, self.utilisateur)
        self.assertTrue(ct1!=self.bloc2.get_coinbase_transaction())



