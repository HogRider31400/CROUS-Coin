import sys
sys.path.append("../.")
from Signature import Signature
from Transaction import Transaction
import unittest

class testTransaction(unittest.TestCase):

    def setUp(self):
        '''--50-->Alice--30-->Bob'''
        self.sigAcheteur = Signature(6860330711641493838657733384476358629162647833562217184859840287317898912502689148572560166805056128767095421205808998005448039984877971935931762873293694, 3609535929987203074032861871981108126642716889100519307328931499450441962218057698861346955485805345401403119102302006282998999305030249203985919489288768)
        self.sigVendeur = Signature(5404610268789347304849272272277944547036425260513460202903728858199590904320942746833327857902924073979681901552585249785761273976696878058492205121792659, 5632639444325148124331431899433974853976554267230705405685206076044188396207430942928661881032631678801713123759819813020853061050974969433904558624768588)
        self.tabI = [{"montant":50,"sigAcheteur":self.sigAcheteur,"cleAcheteur":(8667227302312745347989796666811043245293172756660426488620923220903634571126833772106013721563508400129372997683480234871666992401865215262064169851808577, 478542867424640509862813356325072670548301147791883925111643152919867128924637143027678715392826421537367278348543527890751053865131854828852483615107260)}]
        self.tabO = [{"vendeur":"Bob","montant":30,"sigVendeur":self.sigVendeur,"cleVendeur":(6423001988954252172405372139523251845718594024544172847032849082592103128071335619632140648935050423451312699190924284706492879994521331880951913520302930, 5314414441985343488632619409409454076245649709322575716304421636043959006640450033684616507434319151603176743153677173917274496178327793255219139242837772)}]
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