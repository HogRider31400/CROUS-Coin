import json
import time
import sys
sys.path.append("..")
from Signature import Signature

class Transaction:

    #Attributs : horodatage, inputs, outputs
    outputs = []

    ##Une input est de la forme : {vendeur:...(adresse),montant:...,sigVendeur:...(signature)}
    ##Une output est de la forme : {acheteur:...,montant:...,sigAcheteur:...}

    #S'ASSURER QUE LES INPUTS VIENNENT BIEN TOUTES DE L'UTXO SET

    def __init__(self, inputs, outputs):
        self.horodatage = time.time()
        self.inputs = inputs
        self.outputs = outputs
        self.nbInputs = len(inputs)
        self.nbOutputs = len(outputs)

    @classmethod
    def from_text(cls,text):
        bloc_data = json.loads(text)

        horodatage = bloc_data["horodatage"]
        inputs = bloc_data["inputs"]
        outputs = bloc_data["outputs"]

        return cls(horodatage,inputs,outputs)

    def __repr__(self):
        return "Transaction ("+horodatage+"-I:"+afficherIO(inputs)+"-O:"+afficherIO(outputs)+')'

    def ajouterInputs(newInputs):
        '''Entrée : prend un tableau d'inputs, (les vérifie une à une?) puis les ajoute
        dans les inputs de la transaction'''
        ##vérifier que dans l'UTXO set
        inputs = inputs + newInputs
        nbInputs += len(newInputs)

    def enleverInputs(delInputs):
        trouve = False
        result = []
        for oldInput in delInputs:
            i=0
            while (i<nbInputs and not trouve):
                if (inputs[i] == oldInput):
                    del inputs[i]
                    trouve = True
                    result.append(True)
                i+=1
            if (not trouve):
                result.append(False)
                trouve = False
        return result

    def ajouterOutputs(newOutputs):
        '''Entrée : prend un tableau d'outputs, (les vérifie une à une?) puis les ajoute
        dans les outputs de la transaction'''
        ##vérifier que dans l'UTXO set
        outputs = outputs + newOutputs
        nbOutputs += len(newOutputs)

    def enleverOutputs(delOutputs):
        trouve = False
        result = []
        for output in delOutputs:
            i=0
            while (i<nbOutputs and not trouve):
                if (outputs[i] == output):
                    del outputs[i]
                    trouve = True
                    result.append(True)
                i+=1
            if (not trouve):
                result.append(False)
                trouve = False
        return result


    def afficherIO(tabIO):
        '''Permet d'afficher un tableau d'entrées ou de sorties'''
        bills = ""
        for bill in tabIO:
            bills += bill.toString()+','
        if (bills.length()!=0):
            bills = bills[:-1]
        return bills

    def differenceIO():
        sommeI = 0
        sommeO = 0
        for billI in inputs:
            sommeI += billI["montant"]
        for billO in outputs:
            sommeO += billO["montant"]
        return sommeI - sommeO

    ##Vérification

    def verifier():
        #Ajouter vérification avec UTXO set et l'histoire des clés ? (vérifier les signatures ???)
        return sommePositive() and verifierSignatures()

    def sommePositive():
        return differenceIO()>=0

    def verifierSignatures():
        return verifierSigInputs() and verifierSigOutputs()

    def verifierSigInputs():
        valide = True
        for bill in inputs:
            valide = valide and bill["sigVendeur"].verifier()
        return valide

    def verifierSigOutputs():
        valide = True
        for bill in outputs:
            valide = valide and bill["sigAcheteur"].verifier()
        return valide



    ##Getteurs
    #Pas de set sur l'horodatage pour éviter les fraudes

    def getHorodatage():
        return horodatage

    def getInputs():
        return inputs

    def getOutputs():
        return outputs

    def setInputs(newInputs):
        inputs = newInputs
        nbInputs = len(newInputs)

    def setOutputs(newOutputs):
        outputs = newOutputs
        nbOutputs = len(newOutputs)