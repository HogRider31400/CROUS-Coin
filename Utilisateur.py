import sys
sys.path.append("./Blockchain")
sys.path.append("./EllipticCurves")


from ClePrivee import ClePrivee
from UTXOSet import UTXOSet
from Transaction import Transaction
from Signature import Signature

class Utilisateur:

    NBMAXINPUTS = 1000
    NBMAXOUTPUTS = 1000

    def __init__(self,private_key):
        self.private_key = ClePrivee(private_key)
        self.wallet = ','.join([str(cur) for cur in self.private_key.point.get_coords()])
        self.init_blockchain()
        self.menu()

    def init_blockchain(self):
        
        try:
            with open("./Blockchain/utxo/data") as f:
                set_data = f.read()
        except:
            with open("./Blockchain/utxo/data","w") as f:
                pass
            set_data = ""

        self.utxo_set = UTXOSet(set_data, False,'./Blockchain/utxo/','./Blockchain/blocs/')

    def creer_transaction(self,inputs, outputs, horodatage=None):
        return Transaction(inputs, outputs, self.wallet, horodatage)
    
    def afficher_transactions_anterieures(self):
        print("Vos transactions : blablabla à récupérer de l'UTXO Set....")

    def entrer_un_nombre(self,message,min,max=-1):
        userInput = min - 1
        while (userInput < min or (userInput > max or max ==-1)):
            try:
                msg = "Veuillez entrer " + message
                if (max != -1):
                    msg += " (entre " + min + " et " + max + ") :"
                userInput = int(input(msg))
            except:
                print("Cette entrée ne correspond pas à un chiffre.\n")
        return userInput
    
    def entrer_input(self, transaction):
        montant = self.entrerUnNombre("le montant",0)

        vieilles_outputs = self.utxo_set.get_user_utxos(self.wallet)
        trouve = False
        i=0
        while(i<len(vieilles_outputs) and not trouve):
            vieille_output = vieilles_outputs[i]
            if (vieille_output["montant"] == montant):
                trouve = True
            i+=1
        input = transaction.creerUneInputDico(self, montant, vieille_output["sigVendeur"], vieille_output["cleVendeur"])
        transaction.ajouterInputs([input])
    
    def entrer_output(self, transaction):
        montant = self.entrerUnNombre("le montant",0)
        adresseVendeur = input("Entrez l'adresse de celui à qui vous voulez donner de l'argent :")
        input = transaction.creerUneInputDico(self, montant, "sigVendeur", "cleVendeur")
        transaction.ajouterInputs([input])

    def menu_transaction(self):
        transaction = self.creerTransaction([],[])
        self.afficherTransactionsAnterieures()
        nbTransAnterieures = self.entrerUnNombre("le nombre de transactions que vous souhaitez utiliser :",1,self.NBMAXINPUTS)
        for i in range(nbTransAnterieures):
            self.entrerInput(transaction)
        
        nbDepenses = self.entrerUnNombre("le nombre de dépenses que vous comptez faire avec cet argent :",0,self.NBMAXOUTPUTS)
        for j in range(nbDepenses):
            self.entrerOutput(transaction)

    def menu(self):

        message_debut = [
            "Votre wallet est " + self.wallet,
            "Vous pouvez :",
            "0 : Consulter votre solde",
            "1 : Faire une transaction",
            "2 : Miner",
            "3 : Mettre à jour la blockchain",
            "4 : Quitter",
            "Votre choix : "
        ]

        choix_possibles = set([0,1,2,3,4])

        while True:
            
            choix = -1
            while not choix in choix_possibles:
                choix = input("\n".join(message_debut))
                try:
                    choix = int(choix)
                except:
                    choix = -1

            if choix==1:
                self.menuTransaction()
            elif choix==4: return
            elif choix == 0:
                print("Votre solde est :",sum(self.utxo_set.get_block_utxos(self.wallet)))

            else:
                print("Jsp pas implémenté")

a = Utilisateur(2)