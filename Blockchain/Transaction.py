import json
import time

class Transaction:

    #Attributs : horodatage, inputs, outputs
    inputs = []

    ##Une input est de la forme : (adresseDepenseur,montant,signatureReceveur)
    ##Une output est de la forme : (adresseReceveur,montant,signatureDepenseur)

    #S'ASSURER QUE LES INPUTS VIENNENT BIEN TOUTES DE L'UTXO SET

    def __init__(self, input1):
        self.horodatage = time.time()
        self.inputs.append(input1) #chaque transaction amène forcément de l'argent
        self.outputs = []
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
        nbInputs += newInputs.length()

    def enleverInputs(delInputs):
        result = []
        for oldInput in delInputs:
            for i in range(nbInputs):
                if (inputs[i] == oldInput):
                    del inputs[i]
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

    ##Getteurs
    #Pas de set sur l'horodatage pour éviter les fraudes

    def getHorodatage():
        return horodatage

    def getInputs():
        return inputs

    def getOutputs():
        return outputs