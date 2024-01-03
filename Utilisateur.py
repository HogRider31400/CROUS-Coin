import sys
sys.path.append("./Blockchain")
sys.path.append("./EllipticCurves")


from ClePrivee import ClePrivee
from UTXOSet import UTXOSet

class Utilisateur:

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

    def menu(self):

        message_debut = [
            "Votre wallet est " + self.wallet,
            "Vous pouvez faire :",
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


            if choix==4: return
            elif choix == 0:
                print("Votre solde est :",sum(self.utxo_set.get_block_utxos(self.wallet)))

            else:
                print("Jsp pas implémenté")

a = Utilisateur(2)