import json
import time
import sys
import utils
sys.path.append("..")
from utils.py import *
from Signature import Signature
from Point import Point

N = order
G = Point(generator_x,generator_y)

class Transaction:

    #Attributs : horodatage, inputs, outputs, nbInputs, nbOutputs, adresse

    ##Une input est de la forme : {montant:...,sigAcheteur:...(signature),cleAcheteur:...(Px,Py)}
    ##Une output est de la forme : {vendeur:...,montant:...,sigVendeur:...,cleVendeur:...(Px,Py)}

    '''
    Principe :
        Lorsque Bob veut acheter quelque chose avec des CrousCoin, il amène sur
        la table l'ensemble des transactions dont il ne s'est pas servi où il a reçu
        de l'argent. Ce sont les inputs.

        Dans une input il y a l'adresse de celui qui lui a acheté qqch (ou rendu un
        service dans la vraie vie), le montant de l'achat, l'adresse de Bob (qui avait le
        rôle de vendeur), et la signature de Bob.

        On rajoute pour plus de commodité la clé publique de Bob dans chaque input.

        ->B->C
        et dans l'UTXO set : ->C
    '''

    #S'ASSURER QUE LES INPUTS VIENNENT BIEN TOUTES DE L'UTXO SET

    def __init__(self,inputs, outputs, adresseAcheteur):
        self.horodatage = time.time()
        self.inputs = inputs
        self.outputs = outputs
        self.nbInputs = len(inputs)
        self.nbOutputs = len(outputs)
        self.adresseAcheteur = adresseAcheteur

    @classmethod
    def from_text(cls,text):
        bloc_data = json.loads(text)

        self.horodatage = bloc_data["horodatage"]
        self.inputs = bloc_data["inputs"]
        self.outputs = bloc_data["outputs"]

        return cls(self.horodatage,self.inputs,self.outputs)

    def __repr__(self):
        return "Transaction ("+self.horodatage+"-I:"+afficherIO(self.inputs)+"-O:"+afficherIO(self.outputs)+')'

    def ajouterInputs(self,newInputs):
        '''Entrée : prend un tableau d'inputs, (les vérifie une à une?) puis les ajoute
        dans les inputs de la transaction'''
        ##vérifier que dans l'UTXO set
        self.inputs = self.inputs + newInputs
        self.nbInputs += len(newInputs)

    def enleverInputs(self,delInputs):
        trouve = False
        result = []
        for oldInput in delInputs:
            i=0
            while (i<nbInputs and not trouve):
                if (self.inputs[i] == oldInput):
                    del self.inputs[i]
                    trouve = True
                    result.append(True)
                i+=1
            if (not trouve):
                result.append(False)
                trouve = False
        return result

    def ajouterOutputs(self,newOutputs):
        '''Entrée : prend un tableau d'outputs, (les vérifie une à une?) puis les ajoute
        dans les outputs de la transaction'''
        ##vérifier que dans l'UTXO set
        self.outputs = self.outputs + newOutputs
        self.nbOutputs += len(newOutputs)

    def enleverOutputs(self,delOutputs):
        trouve = False
        result = []
        for output in delOutputs:
            i=0
            while (i<self.nbOutputs and not trouve):
                if (self.outputs[i] == output):
                    del self.outputs[i]
                    trouve = True
                    result.append(True)
                i+=1
            if (not trouve):
                result.append(False)
                trouve = False
        return result


    def afficherIO(self,tabIO):
        '''Permet d'afficher un tableau d'entrées ou de sorties'''
        bills = ""
        for bill in tabIO:
            bills += str(bill)+','
        if (len(bills)!=0):
            bills = bills[:-1]
        return bills

    def differenceIO(self):
        sommeI = 0
        sommeO = 0
        for billI in self.inputs:
            sommeI += billI["montant"]
        for billO in self.outputs:
            sommeO += billO["montant"]
        return sommeI - sommeO

    ##Vérification

    def verifier(self):
        #Ajouter vérification avec UTXO set et l'histoire des clés ? (vérifier les signatures ???)
        return sommePositive() and verifierSignatures()

    def sommePositive(self):
        return differenceIO()>=0

    def hasherMsg(self,msg):
        zh = s256(msg.encode('utf-8')).digest()
        z = utils.get_int(zh,N)
        return z

    def verifierSignatures(self):
        return verifierSigInputs() and verifierSigOutputs()

    def verifierSigInputs(self):
        valide = True
        for bill in self.inputs:
            P = bill["cleVendeur"]
            creerMsg(self.horodatage,bill["montant"],self.adresseAcheteur)
            valide = valide and bill["sigVendeur"].verifier(hasherMsg(msg),G,N,P)
        return valide

    def verifierSigOutputs(self):
        valide = True
        for bill in self.outputs:
            P = bill["cleAcheteur"]
            creerMsg(self.horodatage,bill["montant"],bill["vendeur"])
            valide = valide and bill["sigAcheteur"].verifier(hasherMsg(msg),G,N,P)
        return valide

    def creerMsg(self,horodatage,montant,adresse):
        return str(horodatage)+'#'+montant+'#'+adresse


    ##Getteurs
    #Pas de set sur l'horodatage pour éviter les fraudes

    def getHorodatage(self):
        return self.horodatage

    def getInputs(self):
        return self.inputs

    def getOutputs(self):
        return self.outputs

    def setInputs(self,newInputs):
        self.inputs = newInputs
        self.nbInputs = len(newInputs)

    def setOutputs(self,newOutputs):
        self.outputs = newOutputs
        self.nbOutputs = len(newOutputs)