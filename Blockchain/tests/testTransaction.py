import sys
sys.path.append("../.")
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
        self.sigAcheteur = Signature(10096418555179652889800172204087242434959472080164048694317128684326688312304959089149065794385535341885837182932711796094008306581973946785495755007085897, 3781219854038673287920455390128527499525682462624307699333647319293301497464955898438546599344688368977087543893209100913746220346856893219447814518475156)
        self.cleAcheteur = Point(8667227302312745347989796666811043245293172756660426488620923220903634571126833772106013721563508400129372997683480234871666992401865215262064169851808577, 478542867424640509862813356325072670548301147791883925111643152919867128924637143027678715392826421537367278348543527890751053865131854828852483615107260,CE)
        self.sigVendeur = Signature(5193054151796020867796079317215895125416954011520737686212933464193688844163720022049989770783145768651490039855648267264998506634610315284796067939163192, 948862057077238869355070715155661215666070883659257880635117085055413579907218370297126736836643352013794303480638654157685636174972678800694203418673094)
        self.cleVendeur = Point(6423001988954252172405372139523251845718594024544172847032849082592103128071335619632140648935050423451312699190924284706492879994521331880951913520302930, 5314414441985343488632619409409454076245649709322575716304421636043959006640450033684616507434319151603176743153677173917274496178327793255219139242837772,CE)
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
        inputEncap = [self.paiementAB.creerUneInputDico(50, (3,4), (45,46))]
        self.paiementAB.ajouterInputs(inputEncap)
        self.assertEqual(2, len(self.paiementAB.getInputs()))
        self.paiementAB.enleverInputs(inputEncap)
        self.assertEqual(1, len(self.paiementAB.getInputs()))
    
    def testAjouterSupprimerOutputs(self):
        outputEncap = [self.paiementAB.creerUneOutputDico("Bob",50, (3,4), (45,46))]
        self.paiementAB.ajouterOutputs(outputEncap)
        self.assertEqual(2, len(self.paiementAB.getOutputs()))
        self.paiementAB.enleverOutputs(outputEncap)
        self.assertEqual(1, len(self.paiementAB.getOutputs()))

    def testVerifier(self):
        self.assertTrue(self.paiementAB.verifier())