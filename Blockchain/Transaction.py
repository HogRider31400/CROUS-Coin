class Transaction:

    #Attributs : horodatage, inputs, outputs
    inputs = []

    ##Une input est de la forme : (adresseDepenseur,montant,signatureReceveur)
    ##Une output est de la forme : (adresseReceveur,montant,signatureDepenseur)

    #S'ASSURER QUE LES INPUTS VIENNENT BIEN TOUTES DE L'UTXO SET

    def __init__(self, horodatage, input1):
        self.horodatage = horodatage
        self.inputs.append(input1) #chaque transaction amène forcément de l'argent
        self.outputs = []
        self.nbInputs = 1
        self.nbOutputs = 0

    @classmethod
    def from_text(cls,text):
        return cls()

    def __repr__(self):
        return "Transaction ("+horodatage+"-I:"+afficherIO(inputs)+"-O:"+afficherIO(outputs)+')'

    def ajouterInputs(newInputs):
        '''Entrée : prend un tableau d'inputs, (les vérifie une à une?) puis les ajoute
        dans les inputs de la transaction'''
        ##vérifier que dans l'UTXO set
        inputs = inputs + newInputs
        nbInputs += newInputs.length()

    def ajouterOutputs(newOutputs):
        '''Entrée : prend un tableau d'outputs, (les vérifie une à une?) puis les ajoute
        dans les outputs de la transaction'''
        ##vérifier que dans l'UTXO set
        outputs = outputs + newOutputs
        nbOutputs += newOutputs.length()

    def afficherIO(tabIO):
        '''Permet d'afficher un tableau d'entrées ou de sorties'''
        bills = ""
        for bill in tabIO:
            bills += bill.toString()+','
        if (bills.length()!=0):
            bills = bills[:-1]
        return bills