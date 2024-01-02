import json
import time
import sys
sys.path.append("..")
import utils
from UTXOSet import UTXOSet
from Signature import Signature
from Point import Point

N = utils.order
G = Point(utils.generator_x,utils.generator_y,utils.CourbeElliptique(*utils.courbe))

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

    utxo_set = UTXOSet()

    def __init__(self,inputs, outputs, adresseAcheteur, horodatage=None):
        if (horodatage == None):
            self.horodatage = time.time()
        self.inputs = inputs
        self.outputs = outputs
        self.nbInputs = len(inputs)
        self.nbOutputs = len(outputs)
        self.adresseAcheteur = adresseAcheteur

    @classmethod
    def from_text(cls,text):
        bloc_data = json.loads(text)

        horodatage = bloc_data["horodatage"]
        adresse_acheteur = bloc_data["acheteur"]
        inputs_data = bloc_data["inputs"]
        inputs = []

        for cur_input in inputs_data:

            new_cur = cur_input

            new_cur["cleAcheteur"] = Point(cur_input["cleAcheteur"][0],cur_input["cleAcheteur"][1],CourbeElliptique(*courbe))
            new_cur["sigAcheteur"] = Signature(cur_input["sigAcheteur"][0],cur_input["sigAcheteur"][1])
            inputs.append(new_cur)

        outputs_data = bloc_data["outputs"]
        outputs = []

        for cur_output in outputs_data:

            new_cur = cur_output

            new_cur["cleVendeur"] = Point(cur_input["cleVendeur"][0],cur_input["cleVendeur"][1],CourbeElliptique(*courbe))
            new_cur["sigVendeur"] = Signature(cur_input["sigVendeur"][0],cur_input["sigVendeur"][1])
            outputs.append(new_cur)


        outputs = bloc_data["outputs"]

        return cls(horodatage,inputs,outputs,adresse_acheteur)
    
    def afficherIO(self,tabIO):
        '''Permet d'afficher un tableau d'entrées ou de sorties'''
        bills = ""
        for bill in tabIO:
            bills += str(bill)+','
        if (len(bills)!=0):
            bills = bills[:-1]
        return bills

    def __repr__(self):
        return "Transaction ("+self.horodatage+"-I:"+self.afficherIO(self.inputs)+"-O:"+self.afficherIO(self.outputs)+')'

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
            while (i<self.nbInputs and not trouve):
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
        valide = self.sommePositive() and self.verifierSignatures()
        for bill in self.inputs:
            valide = valide and self.verifierDansUtxoSet(bill["sigAcheteur"])
        return valide

    def verifierCoinBaseTransaction(self):
        return (len(self.inputs) == 0) and (len(self.outputs) == 1) and self.verifierSigOutputs()

    def verifierDansUtxoSet(self,sig):
        return utxo_set.is_spent(sig)

    def sommePositive(self):
        return self.differenceIO()>=0

    def hasherMsg(self,msg):
        zh = s256(msg.encode('utf-8')).digest()
        z = utils.get_int(zh,N)
        return z

    def verifierSignatures(self):
        return self.verifierSigInputs() and self.verifierSigOutputs()

    def verifierSigInputs(self):
        valide = True
        for bill in self.inputs:
            P = bill["cleVendeur"]
            self.creerMsg(self.horodatage,bill["montant"],self.adresseAcheteur)
            valide = valide and bill["sigVendeur"].verifier(self.hasherMsg(msg),G,N,P)
        return valide

    def verifierSigOutputs(self):
        valide = True
        for bill in self.outputs:
            P = bill["cleAcheteur"]
            self.creerMsg(self.horodatage,bill["montant"],bill["vendeur"])
            valide = valide and bill["sigAcheteur"].verifier(self.hasherMsg(msg),G,N,P)
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