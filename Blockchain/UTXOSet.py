
"""
Classe UTXOSet

Attributs :
    - arbre : l'arbre des transactions/sous-transactions, pour éviter de devoir charger trop de données il n'y a que les noeuds de surface/presque-surface qui seront gardés. Tout noeud complètement recouvert sera supprimé de l'arbre, l'arbre est la structure qui est utilisée pour maintenir à jour l'UTXO set et ne doit pas être accédé de l'extérieur
    - registre : un dictionnaire décliné en 3 version :
        - une version sig où une signature amène vers l'utilisateur et le montant + l'id de transaction
        - une version user où il amène à la liste de tout ce que l'utilisateur a à disposition
        - une version block_hash qui à partir du hash d'un bloc permet de savoir ce qui est encore à disposition dans le bloc (optionnel à mon avis)
    - current_block_hash : le bloc pour lequel le registre est à jour

Méthodes :
    - des getters pour accéder au registre proprement (aucun setter)
    - update : essaye de se mettre à jour en regardant le numéro du dernier bloc et va, bloc non suivi par block non suivi, mettre à jour son arbre puis finalement mettre à jour le registre
    - to_text : transforme l'utxo set sous forme de texte pour être stocké (persistence) et réutilisé, cela évite de recréer constamment un nouvel arbre
Constructeurs :
    - Idéalement uniquement à partir de texte, la chaine vide signifiant un utxo set vide. L'UTXO set tient un registre persistent et n'a donc pas besoin d'être créé à partir de données existantes car sinon il existe déjà (paradoxe de l'UTx07). Il aura aussi une option pour se mettre à jour lors de la construction de l'objet ou pas
"""
def to_str(e):
    return ','.join([str(x) for x in e])

import json
import os
import copy
import math
import sys
sys.path.append("./blocs")
sys.path.append("..")


class UTXOSet:

    def __init__(self,texte, update=False,BLOC_FOLDER = './blocs/',UTXO_FOLDER = './utxo/'):
        self.BLOC_FOLDER = BLOC_FOLDER
        self.UTXO_FOLDER = UTXO_FOLDER
        self.load_set(texte)
        if update:
            self.update_all()

    def load_set(self,texte):
        if texte == "" or texte == {}:
            self.arbre = {}
            self.registre = {
                "user" : {},
                "sig" : {},
                "block_hash" : {},
                "block_height" : {}
            }
            self.hauteur = 0
            self.blocks_timestamps = []
            self.current_block_hash = None
            self.save()
        else:
            if type(texte) != dict:
                set_data = json.loads(texte)
            else:
                set_data = texte #déjà du json
            
            self.arbre = set_data["arbre"]
            self.hauteur = set_data["hauteur"]
            self.registre = set_data["registre"]
            self.blocks_timestamps = set_data["blocks_timestamps"]
            self.current_block_hash = set_data["current_block_hash"]

    def get_next_block(self):
        
        block_list = os.listdir(self.BLOC_FOLDER)

        for block_hash in block_list:

            with open(self.BLOC_FOLDER+block_hash) as f:
                content = f.read()
                content_data = json.loads(content)
                if content_data["previous_block_hash"] == self.current_block_hash:
                    return block_hash
        return None

    def update_next_block(self):
        next_block_hash = self.get_next_block()
        if not (next_block_hash):
            return 3

        with open(self.BLOC_FOLDER+next_block_hash) as f:
            next_block_content = f.read()
        next_block_data = json.loads(next_block_content)
        #print("MIIIIISE A JOUR")
        #print(next_block_data)
        self.current_block_hash = next_block_hash

        for transaction in next_block_data["transactions"]:
            success = self.try_update_tree(transaction)
            if not success:
                print("Block", next_block_hash ,"is not OK, current block is still",self.current_block_hash)
                self.rollback()
                return False
        success = self.try_update_tree(next_block_data["coinbase_transaction"])
        if not success:
            print("Block", next_block_hash ,"is not OK, current block is still",self.current_block_hash)
            self.rollback()
            return False

        self.hauteur += 1
        self.registre["block_height"][next_block_hash] = self.hauteur
        self.blocks_timestamps.append(next_block_data["timestamp"])
        return True

    def update_all(self,reset=False):
        if reset:
            self.load_set("")
        cur = True
        while cur == True:
            cur = self.update_next_block()
            #print("Cur block is now ",self.current_block_hash)
            self.save()
        
        if cur == 3:
            return True
        return False

    def update_tree(self,transaction):


        copie_arbre = copy.deepcopy(self.arbre)

        outputs = transaction["outputs"]
        inputs = transaction["inputs"]

        for cur_input in inputs:
            #print("cur input est")
            #print(cur_input)
            #print(copie_arbre.keys())
            if to_str(cur_input["sigAcheteur"]) in copie_arbre:
                #TODO : mettre à jour le registre
                del copie_arbre[to_str(cur_input["sigAcheteur"])]
            else:
                return False # ce n'est pas un utxo et n'a rien à faire en input

        for cur_output in outputs:
            if to_str(cur_output["sigVendeur"]) not in copie_arbre:
                #TODO : mettre à jour le registre
                copie_arbre[to_str(cur_output["sigVendeur"])] = cur_output
            else:
                return False # duplication de signature en output, il y a eu une erreur de transmission
                             #ou le vendeur essaye d'enfler l'acheteur
        self.arbre = copie_arbre
        self._update_registre(transaction)
        return True

    def _update_registre(self,transaction):

        #Méthode "interne", on part du principe qu'elle est appelée que dans update_tree et jamais de l'extérieur
        #Donc les données de "transaction" sont valides et il ne devrait y avoir aucune erreur lors de la mise à jour du registre

        acheteur = transaction["acheteur"]
        # Partie 1 : on enlève les éléments dans l'input
        for cur_input in transaction["inputs"]:
            del self.registre["sig"][to_str(cur_input["sigAcheteur"])]

            index_user_remove = -1
            for i in range(len(self.registre["user"][acheteur])):
                elem = self.registre["user"][acheteur][i]
                if to_str(elem["sigVendeur"]) == to_str(cur_input["sigAcheteur"]):
                    index_user_remove = i
                    break

            self.registre["user"][acheteur].pop(index_user_remove)
            if(len(self.registre["user"][acheteur]) == 0):
                del self.registre["user"][acheteur]
            
            if self.current_block_hash in self.registre["block_hash"]:
                index_block_remove = -1
                for i in range(len(self.registre["block_hash"][self.current_block_hash])):
                    elem = self.registre["block_hash"][self.current_block_hash][i]
                    if to_str(elem["sigVendeur"]) == to_str(cur_input["sigAcheteur"]):
                        index_block_remove = i
                        break

                self.registre["block_hash"][self.current_block_hash].pop(index_block_remove)
            
        #Partie 2 : on ajoute les nouveaux
        for cur_output in transaction["outputs"]:

            cur_output.update({"horodatage" : transaction["horodatage"]})

            self.registre["sig"][to_str(cur_output["sigVendeur"])] = cur_output
            if not cur_output["vendeur"] in self.registre["user"]:
                self.registre["user"][cur_output["vendeur"]] = []
            self.registre["user"][cur_output["vendeur"]].append(cur_output)
            if not self.current_block_hash in self.registre["block_hash"]:
                self.registre["block_hash"][self.current_block_hash] = []
            self.registre["block_hash"][self.current_block_hash].append(cur_output)
            #TODO : partie block_hash
    
    def get_hauteur(self):
        return self.hauteur

    def is_spent(self,sig):
        if to_str(sig) in self.registre["sig"]:
            return False
        return True

    def get_sig_h(self,sig):
        print("ON RETOURNE ",self.registre["sig"][to_str(sig)]["horodatage"])
        if to_str(sig) in self.registre["sig"]:
            return self.registre["sig"][to_str(sig)]["horodatage"]
        return 0

    def get_user_utxos(self,user):
        #print(user,self.registre["user"])
        if user in self.registre["user"]:
            return self.registre["user"][user]
        return []

    def get_block_utxos(self,block_hash):
        if block_hash in self.registre["block_hash"]:
            return self.registre["block_hash"][block_hash]
        return []

    def try_update_tree(self,transaction):
        update_success = self.update_tree(transaction)
        return update_success

    def rollback(self):
        with open(self.UTXO_FOLDER+"data") as f:
            last_saved_content = f.read()
            self.load_set(last_saved_content)

    def get_mining_mean(self,block_height):
        
        if len(self.blocks_timestamps) < 10:
            return None
        else:
            diff_s = 0
            for i in range(block_height-9,block_height):
                diff_s += self.blocks_timestamps[i] - self.blocks_timestamps[i-1] 
            return (diff_s/60)/10

    def get_mining_difficulty(self,block_hash=None):
        
        if not block_hash:
            block_height = self.hauteur
        else:
            block_height = self.registre["block_height"][block_hash]
        x = self.get_mining_mean(block_height)
        if not x:
            x = 2
        f = lambda x: math.floor(-(8*x/21 - 1.5)**3 + 5)
        y = f(x)

        if y < 3:
            y = 3
        return y

    def save(self):

        new_set_data = {
            "arbre" : self.arbre,
            "registre" : self.registre,
            "current_block_hash" : self.current_block_hash,
            "hauteur" : self.hauteur,
            "blocks_timestamps" : self.blocks_timestamps
        }

        new_set_content = json.dumps(new_set_data)
        with open(self.UTXO_FOLDER+"data","w") as f:
            f.write(new_set_content)