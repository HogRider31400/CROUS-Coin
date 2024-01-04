import json
import time
import hashlib
import sys
sys.path.append("..")
sys.path.append("../EllipticCurves")
import utils
from UTXOSet import UTXOSet
from Signature import Signature
from Point import Point
from CourbeElliptique import CourbeElliptique

N = utils.order
G = Point(utils.generator_x,utils.generator_y,CourbeElliptique(*utils.courbe))

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

    def __init__(self,inputs, outputs, adresseAcheteur, horodatage=None,utxo_set=""):
        self.utxo_set = utxo_set
        if (horodatage == None):
            self.horodatage = time.time()
        else :
            self.horodatage = horodatage
        self.inputs = inputs
        self.outputs = outputs
        self.nbInputs = len(inputs)
        self.nbOutputs = len(outputs)
        self.adresseAcheteur = adresseAcheteur

    @classmethod
    def from_text(cls,text,utxo_set=""):
        if type(text) != dict:
            bloc_data = json.loads(text)
        else:
            bloc_data = text
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
        return "Transaction ("+str(self.horodatage)+"-I:"+self.afficherIO(self.inputs)+"-O:"+self.afficherIO(self.outputs)+')'

#------------------------------------------------------------------------------------------------------------------
# Gestion des Inputs / Outputs
#------------------------------------------------------------------------------------------------------------------
    
    def ajouter_inputs(self,newInputs):
        '''Entrée : prend un tableau d'inputs, (les vérifie une à une?) puis les ajoute
        dans les inputs de la transaction'''
        ##vérifier que dans l'UTXO set
        self.inputs = self.inputs + newInputs
        self.nbInputs += len(newInputs)

    def enlever_inputs(self,delInputs):
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

    def ajouter_outputs(self,newOutputs):
        '''Entrée : prend un tableau d'outputs, (les vérifie une à une?) puis les ajoute
        dans les outputs de la transaction'''
        ##vérifier que dans l'UTXO set
        self.outputs = self.outputs + newOutputs
        self.nbOutputs += len(newOutputs)

    def enlever_outputs(self,delOutputs):
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

#------------------------------------------------------------------------------------------------------------------
# Vérification
#------------------------------------------------------------------------------------------------------------------


    ##Calculer la différence entre le montant des inputs / outputs
    def differenceIO(self):
        sommeI = 0
        sommeO = 0
        for billI in self.inputs:
            sommeI += billI["montant"]
        for billO in self.outputs:
            sommeO += billO["montant"]
        return sommeI - sommeO
    
    def creer_msg(self,horodatage,montant,adresse):
        return str(horodatage)+'#'+str(montant)+'#'+adresse

    def verifier_coinBase_transaction(self):
        return (len(self.inputs) == 0) and (len(self.outputs) == 1) and self.verifier_sig_outputs()

    def verifier_dans_utxoSet(self,sig):
        return self.utxo_set.is_spent(sig)

    def somme_positive(self):
        return self.differenceIO()>=0

    def hasher_msg(self,msg):
        zh = hashlib.sha512(msg.encode('utf-8')).digest()
        z = utils.get_int(zh,N)
        return z

    def verifier_signatures(self):
        return self.verifier_sig_inputs() and self.verifier_sig_outputs()

    def verifier_sig_inputs(self):
        valide = True
        for bill in self.inputs:
            print(bill)
            P = bill["cleAcheteur"]
            msg = self.creer_msg(self.horodatage,bill["montant"],self.adresseAcheteur)
            print(bill["sigAcheteur"].verifier(self.hasher_msg(msg),G,N,P))
            valide = valide and bill["sigAcheteur"].verifier(self.hasher_msg(msg),G,N,P)
        return valide

    def verifier_sig_outputs(self):
        valide = True
        for bill in self.outputs:
            P = bill["cleVendeur"]
            msg = self.creer_msg(self.horodatage,bill["montant"],bill["vendeur"])
            valide = valide and bill["sigVendeur"].verifier(self.hasher_msg(msg),G,N,P)
        return valide
    
    def verifier(self):
        valide = self.somme_positive() and self.verifier_signatures()
        #for bill in self.inputs:
        #    valide = valide and self.verifierDansUtxoSet(bill["sigAcheteur"])
        return valide


#------------------------------------------------------------------------------------------------------------------
# Getteurs
#------------------------------------------------------------------------------------------------------------------

    #Pas de set sur l'horodatage pour éviter les fraudes

    def get_horodatage(self):
        return self.horodatage

    def get_inputs(self):
        return self.inputs

    def get_outputs(self):
        return self.outputs
    
#------------------------------------------------------------------------------------------------------------------
# Setteurs
#------------------------------------------------------------------------------------------------------------------


    def set_inputs(self,newInputs):
        self.inputs = newInputs
        self.nbInputs = len(newInputs)

    def set_outputs(self,newOutputs):
        self.outputs = newOutputs
        self.nbOutputs = len(newOutputs)

#------------------------------------------------------------------------------------------------------------------
# Création I/O
#------------------------------------------------------------------------------------------------------------------

    def creer_une_input_dico(self, montant, sigAcheteur, cleAcheteur):
        return {"montant":montant, "sigAcheteur":sigAcheteur, "cleAcheteur":cleAcheteur}

    def creer_une_output_dico(self, vendeur, montant, sigVendeur, cleVendeur):
        return {"vendeur":vendeur, "montant":montant, "sigVendeur":sigVendeur, "cleVendeur":cleVendeur}
    
#------------------------------------------------------------------------------------------------------------------
# Transaction en texte
#------------------------------------------------------------------------------------------------------------------

    def to_text(self):
        if self == None:
            return None
        for cur_input in self.inputs:
            new_input = cur_input 
            new_input["cleAcheteur"] = cur_input["cleAcheteur"].get_coords()
            new_input["sigAcheteur"] = cur_input["sigAcheteur"].get_sig()
            self.inputs.ajouter_inputs([new_input])

        for cur_output in self.outputs:
            new_output = cur_output
            new_output["cleVendeur"] = cur_output["cleVendeur"].get_coords()
            new_output["sigVendeur"] = cur_output["sigVendeur"].get_sig()
            self.outputs.ajouter_inputs([new_output])
            
        dico_trans = {
            "horodatage" : self.horodatage,
            "inputs" : self.inputs,
            "outputs" : self.outputs
        }

        return json.dumps(dico_trans)
