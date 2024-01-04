import sys
sys.path.append("../.")
sys.path.append("../EllipticCurves")
from Signature import Signature
from Transaction import Transaction
from Point import Point
import unittest
from CourbeElliptique import CourbeElliptique
from utils import courbe

CE = CourbeElliptique(*courbe)

class testTransaction(unittest.TestCase):

    def setUp(self):
        '''--50-->Alice--30-->Bob'''
        self.sigAcheteur = Signature(5439102160533729286291568068280253624165601758875954373768139906654721812274359516693644104284664715234766909782804012342090970415733450516337396768657875, 3486100964449987698544044351520014096183120411052438692040586311244810061267024468023696112323354013173659169321654104653757331092616393675757819802075970)
        self.cleAcheteur = Point(3118285745690082516819838297607382631466653731077196052604216247694373586220294590672106850852280689331172015968294762428131521271281940315228083078173564, 10478894441751583738987044209342758263493827312595290610628159206083819451722646942925992412226360091079021427865278944013668768657919161283910205625581649,CE)
        self.sigVendeur = Signature(6239620238231195149935410106005719780248441283951589381887273808500278162300411124053825646994691143222348259078778694483265942818217345172458084101309303, 3915100741136112862853987721242368465758100068649234333395041302415382190493767702954737026378600372852792961824973096328064512786241726473306196095602381)
        self.cleVendeur = Point(8484445204163366193830149330078115049235616364220758419176782190939615781364471782056917011806805156043914601247665778528157581030055621063961460238682051, 3179642056146878138054123425892357801021704685421506102661972210112319209698516560334307705784968320325088423766650553397393695038883968375717204253839574,CE)
        self.tabI = [{"montant":50,"sigAcheteur":self.sigAcheteur,"cleAcheteur":self.cleAcheteur}]
        self.tabO = [{"vendeur":"Bob","montant":30,"sigVendeur":self.sigVendeur,"cleVendeur":self.cleVendeur}]
        self.paiementAB = Transaction(self.tabI,self.tabO, "Alice",3456789.232323)

    '''
    def testParseTx(self):
        
        newTx = Transaction.from_text("")

    def testValidTx(self):
        newTx = Transaction.from_text("")

        self.assertFalse(newTx.get_signature() == newTx.signature)

        #faire au moins un cas où c'est vrai
    '''
        
    def testRepr(self):
        '''On fixe l'horodatage lors de la vérification pour qu'il soit constant'''
        newPaiement = Transaction([{'montant': 50, 'sigAcheteur': Signature (56, 47), 'cleAcheteur': (1, 2)}],[{'vendeur': 'Bob', 'montant': 30, 'sigVendeur': Signature (34, 78), 'cleVendeur': (3, 4)}],"Alice",3456789.232323)
        self.assertEqual("Transaction (3456789.232323-I:{'montant': 50, 'sigAcheteur': Signature (56, 47), 'cleAcheteur': (1, 2)}-O:{'vendeur': 'Bob', 'montant': 30, 'sigVendeur': Signature (34, 78), 'cleVendeur': (3, 4)})",newPaiement.__repr__())

    def testAjouterSupprimerInputs(self):
        inputEncap = [self.paiementAB.creer_une_input_dico(50, (3,4), (45,46))]
        self.paiementAB.ajouter_inputs(inputEncap)
        self.assertEqual(2, len(self.paiementAB.get_inputs()))
        self.paiementAB.enlever_inputs(inputEncap)
        self.assertEqual(1, len(self.paiementAB.get_inputs()))
    
    def testAjouterSupprimerOutputs(self):
        outputEncap = [self.paiementAB.creer_une_output_dico("Bob", 50, (3,4), (45,46))]
        self.paiementAB.ajouter_outputs(outputEncap)
        self.assertEqual(2, len(self.paiementAB.get_outputs()))
        self.paiementAB.enlever_outputs(outputEncap)
        self.assertEqual(1, len(self.paiementAB.get_outputs()))

    def testVerifier(self):
        self.paiementAB = Transaction(self.tabI,self.tabO, "Alice",3456789.232323)
        print("ON VA VERIF")
        self.assertTrue(self.paiementAB.verifier())