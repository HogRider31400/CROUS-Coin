import json
import time

class Transaction:

    #Attributs : horodatage, inputs, outputs
    outputs = []

    ##Une input est de la forme : {acheteur:...(adresse),montant:...,sigVendeur:...(signature)}
    ##Une output est de la forme : {vendeur:...,montant:...,sigAcheteur:...}

    #S'ASSURER QUE LES INPUTS VIENNENT BIEN TOUTES DE L'UTXO SET

    def __init__(self, output):
        self.horodatage = time.time()
        self.inputs = []
        self.outputs.append(output) #chaque transaction donne forcément de l'argent à quelqu'un
        self.nbInputs = 1
        self.nbOutputs = 0

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
        result = []
        for oldInput in delInputs:
            for i in range(nbInputs):
                if (inputs[i] == oldInput):
                    del inputs[i]
                    nbInputs-=1
                    result.append(True)
            result.append(False)
        return result

    def ajouterOutputs(newOutputs):
        '''Entrée : prend un tableau d'outputs, (les vérifie une à une?) puis les ajoute
        dans les outputs de la transaction'''
        ##vérifier que dans l'UTXO set
        outputs = outputs + newOutputs
        nbOutputs += len(newOutputs)

    def enleverOutputs(delOutputs):
        result = []
        for output in delOutputs:
            for i in range(nbOutputs):
                if (outputs[i] == output):
                    del outputs[i]
                    result.append(True)
            result.append(False)
        return result


    def afficherIO(tabIO):
        '''Permet d'afficher un tableau d'entrées ou de sorties'''
        bills = ""
        for bill in tabIO:
            bills += bill.toString()+','
        if (bills.length()!=0):
            bills = bills[:-1]
        return bills


    ##Vérification

    def verifier():
        sommePositive()

    def sommePositive():
        sommeI = 0
        sommeO = 0
        for billI in inputs:
            sommeI += billI["montant"]
        for billO in outputs:
            sommeO += billO["montant"]
        return sommeI >= sommeO

    ##Getteurs
    #Pas de set sur l'horodatage pour éviter les fraudes

    def getHorodatage():
        return horodatage

    def getInputs():
        return inputs

    def getOutputs():
        return outputs