import sys
sys.path.append("./Blockchain")
sys.path.append("./EllipticCurves")
import os

from ClePrivee import ClePrivee
from UTXOSet import UTXOSet
from Transaction import Transaction
from Signature import Signature
from Minage import Minage
from utils_user import dossier_existe,hash_sha256,get_chain_length,CHEMINACCESTX,nb_transac_dernier_bloc
import json
from Bloc import Bloc
from CourbeElliptique import CourbeElliptique
from utils import courbe
from Point import Point
CE = CourbeElliptique(*courbe)

class Utilisateur:

    NBMAXINPUTS = 1000
    NBMAXOUTPUTS = 1000

    def __init__(self,private_key,menu=True):
        self.private_key = ClePrivee(private_key)
        self.wallet = hash_sha256(','.join([str(cur) for cur in self.private_key.point.get_coords()]))
        print(self.wallet)
        self.DOSSIER = "./Users/" + self.wallet + "/"
        self.init_blockchain()
        if menu:
            self.menu()

    #--------------------------------------------------------------------------------
    # BLOCKCHAIN
    #--------------------------------------------------------------------------------

    def init_blockchain(self):
        
        if not dossier_existe("./Users/"):
            os.mkdir("./Users/")

        if not dossier_existe(self.DOSSIER):
            os.mkdir(self.DOSSIER)

        DOSSIER_BLOCS = self.DOSSIER+"blocs/"
        DOSSIER_UTXO = self.DOSSIER+"utxo/"
        
        if not dossier_existe(DOSSIER_BLOCS):
            os.mkdir(DOSSIER_BLOCS)
        if not dossier_existe(DOSSIER_UTXO):
            os.mkdir(DOSSIER_UTXO)
        if not dossier_existe(self.DOSSIER+"temp/"):
            os.mkdir(self.DOSSIER+"temp/")
        try:
            with open(DOSSIER_UTXO+"data") as f:
                set_data = f.read()
        except:
            with open(DOSSIER_UTXO+"data","w") as f:
                pass
            set_data = ""

        self.utxo_set = UTXOSet(set_data, True,DOSSIER_BLOCS,DOSSIER_UTXO)

    def update_blockchain(self):

        cur_blocs = set(os.listdir(self.DOSSIER+"blocs/"))

        user_list = os.listdir("./Users/")
        #print(user_list)
        cur_block_user = self.utxo_set.current_block_hash

        to_check = []

        for user in user_list:
            if user == "transactions_en_cours" or user == self.wallet:
                continue
            user_blocs = os.listdir("./Users/"+user+"/blocs/")
            #print(user,user_blocs)
            blocs_pas_dans = []
            a_info_en_plus = False
            contient_cur_block = True #(cur_block_user == None)
            corresp_graphe = {}

            for cur_bloc in user_blocs:
                
                with open("./Users/"+user+"/blocs/"+cur_bloc) as f:
                    file_data = f.read()
                
                file_content = json.loads(file_data)
                prev_hash = file_content["previous_block_hash"]
                if not prev_hash in corresp_graphe:
                    corresp_graphe[prev_hash] = []
                corresp_graphe[prev_hash].append(cur_bloc)

                #if cur_bloc == cur_block_user:
                #    contient_cur_block = True

                if not cur_bloc in cur_blocs:
                    a_info_en_plus = True
                    blocs_pas_dans.append((cur_bloc,file_content))

            if a_info_en_plus and contient_cur_block:
                #On check que la blockchain a une évolution de son utxo_set valide
                #TODO : optimiser, mais pas le courage là.
                #Piste d'optimisation : partir de l'utxoset que l'utilsateur a et vérifier à partir de là
                #print("SALUUUUUUUUUUUUUUUUUT")
                #print(user)
                is_valid = UTXOSet("",False,self.DOSSIER+"temp/","./Users/"+user+"/blocs/").update_all()
                if is_valid:
                    to_check.append((get_chain_length(corresp_graphe),nb_transac_dernier_bloc(user,blocs_pas_dans),blocs_pas_dans))
        #print("SALUUUUUUUUUUUUUUUT")
        #Soit elle est à jour soit elle est cassée
        if len(to_check) == 0:
            return
        #print(to_check)
        #ici on a que des chaines valides ce qui permet une certaine épuration
        to_check.sort(key=lambda x: x[0])
        max_l = to_check[-1][0]
        #On récupère que ceux avec une hauteur maximale
        to_check = [x for x in to_check if x[0] == max_l]

        #On retrie mais cette fois en fonction de la 2eme variable (nb de transac sur le dernier)
        to_check.sort(key=lambda x: x[1])

        #On récupère que les bons
        max_l = to_check[-1][1]

        #Et on trie par horodatage et prend le max d'horodatage
        to_check.sort(key=lambda x: max(x[2],key = lambda y:y[1]["timestamp"]))

        #On récupère donc le premier élément
        new_elems = to_check[0][2]

        for elem in new_elems:
            with open(self.DOSSIER+"blocs/"+elem[0],"w") as f:
                block_content = json.dumps(elem[1])
                f.write(block_content)
        
        self.utxo_set.update_all(reset=True)
        
    #--------------------------------------------------------------------------------
    # TRANSACTIONS
    #--------------------------------------------------------------------------------

    def creer_transaction(self,inputs, outputs, horodatage=None):
        return Transaction(inputs, outputs, self.wallet, horodatage,utxo_set=self.utxo_set)
    
    def afficher_transactions_anterieures(self):
        print("Vos transactions :\n")
        transactions = self.utxo_set.get_user_utxos(self.wallet)
        for transaction in transactions:
            print("- "+transaction.__repr__()+"\n")

    def entrer_un_nombre(self,message,min,max=-1):
        userInput = min - 1
        while (userInput < min or (userInput > max and max != -1)):
            try:
                msg = "Veuillez entrer " + message
                if (max != -1):
                    msg += " (entre " + str(min) + " et " + str(max) + ") :\n"
                else:
                    msg += " :\n"
                userInput = int(input(msg))
            except:
                print("Cette entrée ne correspond pas à un chiffre.\n")
        return userInput
    
    def entrer_input(self, transaction):
        montant = self.entrer_un_nombre("le montant",0)

        vieilles_outputs = self.utxo_set.get_user_utxos(self.wallet)
        vieille_output = None
        trouve = False
        i=0
        while(i<len(vieilles_outputs) and not trouve):
            vieille_output = vieilles_outputs[i]
            if (vieille_output["montant"] == montant):
                trouve = True
            i+=1
        if (vieille_output != None):
            print("VIEILLE OUTPUT N'EST PAS NONE")
            inputT = transaction.creer_une_input_dico(montant, Signature(*vieille_output["sigVendeur"]), Point(*vieille_output["cleVendeur"],CE))
            transaction.ajouter_inputs([inputT])
        return vieille_output
    
    def entrer_output(self, transaction):
        montant = self.entrer_un_nombre("le montant",0)
        adresseVendeur = input("Entrez l'adresse de celui à qui vous voulez donner de l'argent :")
        msgHashe = transaction.hasher_msg(transaction.creer_msg(transaction.get_horodatage(),montant,adresseVendeur))
        outputT = transaction.creer_une_output_dico(adresseVendeur, montant, self.private_key.signer(msgHashe), self.private_key.point)
        transaction.ajouter_outputs([outputT])
        return True

    def menu_transaction(self):
        trans_invalide = False
        transaction = self.creer_transaction([],[])
        self.afficher_transactions_anterieures()
        nbTransAnterieures = self.entrer_un_nombre("le nombre de transactions que vous souhaitez utiliser :",0,self.NBMAXINPUTS)
        if (nbTransAnterieures == 0):
            self.menu()
        i = 0
        while(i < nbTransAnterieures and not trans_invalide):
            cur_input = self.entrer_input(transaction)
            if (cur_input == None):
                trans_invalide = True
            i+=1

        if (not trans_invalide):
            nbDepenses = self.entrer_un_nombre("le nombre de dépenses que vous comptez faire avec cet argent :",0,self.NBMAXOUTPUTS)
            j = 0
            while(j < nbDepenses and not trans_invalide):
                cur_output = self.entrer_output(transaction)
                if (cur_output == None):
                    trans_invalide = trans_invalide and True
                j+=1
        if (trans_invalide):
            print("Transaction invalide veuillez recommencer. ")
        else:
            transTexte = transaction.to_text()

        ##On sauvegarde transTexte dans un fichier commun
        try:
            with open(CHEMINACCESTX) as f:
                fichier_content = json.loads(f.read())
        except:
            fichier_content = []
        if len(fichier_content) == 5:
            print("Il y a déjà trop de transactions en attente, veuillez recommencer ultérieurement.")
        else:
            fichier_content.append(json.loads(transaction.to_text()))
            
            with open(CHEMINACCESTX,"w") as f:
                f.write(json.dumps(fichier_content))

    def miner(self):
        try:
            with open(CHEMINACCESTX) as f:
                tx_attente = json.loads(f.read())
        except:
            tx_attente = []
                
        nouveau_bloc = {
            "previous_block_hash" : self.utxo_set.current_block_hash,
            "timestamp" : None,               
            "coinbase_transaction" : None,
            "transactions" : tx_attente,
            "pow_number" : None,
            "block_difficulty" : self.utxo_set.get_mining_difficulty()
        }

        bo = Bloc.from_text(json.dumps(nouveau_bloc),self.DOSSIER+"blocs/",self.utxo_set)

        self.mineur = Minage(bo,self.wallet,self)

        self.mineur.miner()

        if not self.mineur.is_obsolete:
            bo.save()
            with open(CHEMINACCESTX) as f:
                datas = f.read()
            try:
                data_content = json.loads(datas)
            except:
                data_content = []
            
            for elem in tx_attente:
                data_content.remove(elem)
            print(data_content)

            with open(CHEMINACCESTX,"w") as f:
                f.write(json.dumps(data_content))

            self.utxo_set.update_next_block()
            self.utxo_set.save()

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
                self.menu_transaction()
            elif choix==2:
                self.miner()

            elif choix==4: return
            elif choix == 0:
                t = self.utxo_set.get_user_utxos(self.wallet)
                s = 0
                #print(t)
                for elem in t:
                    s += elem["montant"]
                print("Votre solde est ",s)
            elif choix == 3:
                self.update_blockchain()
            else:
                print("Jsp pas implémenté")

if __name__ == "__main__":
    a = Utilisateur(3)