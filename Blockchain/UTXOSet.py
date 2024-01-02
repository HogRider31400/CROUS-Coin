
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

import json
import os
import copy

class UTXOSet:

    def __init__(self,texte, update=False):
        self.load_set(texte)
        if update:
            self.update_all()

    def load_set(self,texte):
        if texte == "":
            self.arbre = {}
            self.registre = {}
            self.current_block_hash = None
            self.update_set()
        else:
            set_data = json.loads(texte)

            self.arbre = set_data["arbre"]
            self.registre = set_data["registre"]
            self.current_block_hash = set_data["current_block_hash"]

    def get_next_block():
        
        block_list = os.listdir("./blocs")

        for block_hash in block_list:

            with open("./blocs/"+block_hash) as f:
                content = f.read()
                content_data = json.loads(content)
                if content_data["previous_block_hash"] == self.current_block_hash:
                    return block_hash
        return None

    def update_next_block(self):
        next_block_hash = get_next_block()
        if not (next_block_hash):
            return False
        
        with open("./blocs/"+next_block_hash) as f:
            next_block_content = f.read()
        next_block_data = json.loads(next_block_content)

        self.current_block_hash = next_block_hash

        for transaction in next_block_data["transactions"]:
            success = try_update_tree(transaction)
            if not success:
                print("Block", next_block_hash ,"is not OK, current block is still",self.current_block_hash)
                self.rollback()
                return False


        return True
    
    def update_all(self):
        while self.update_next_block():
            print("Cur block is now ",self.current_block_hash)
            self.save()

    def update_tree(self,transaction):

        copie_arbre = copy.deepcopy(self.arbre)

        outputs = transaction["outputs"]
        inputs = transaction["inputs"]

        for cur_input in inputs:
            if cur_input["sigAcheteur"] in copie_arbre:
                #TODO : mettre à jour le registre
                del copie_arbre[cur_input["sigAcheteur"]]
            else:
                return False # ce n'est pas un utxo et n'a rien à faire en input
        
        for cur_output in outputs:
            if cur_output["sigVendeur"] not in copie_arbre:
                #TODO : mettre à jour le registre
                copie_arbre[cur_output["sigVendeur"]] = cur_output
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
            del registre["sig"][cur_input["sigVendeur"]]

            registre["user"][acheteur].remove(cur_input)
            if(len(registre["user"][acheteur]) == 0):
                del registre["user"][acheteur]
            registre["block_hash"][self.current_block_hash].remove(cur_input)
        
        #Partie 2 : on ajoute les nouveaux
        for cur_output in transaction["outputs"]
            registre["sig"][cur_input["sigVendeur"]] = cur_output
            if not cur_input["vendeur"] in registre["user"]:
                registre["user"][cur_input["vendeur"]] = []
            registre["user"][cur_input["vendeur"]].append(cur_output)
            if not self.current_block_hash in registre["block_hash"]:
                registre["block_hash"][self.current_block_hash] = []
            registre["block_hash"][self.current_block_hash].append(cur_output)
            #TODO : partie block_hash

    def is_spent(self,sig):
        if sig in registre["sig"]:
            return False
        return True
    
    def get_user_utxos(self,user):
        if user in registre["user"]:
            return registre["user"][user]
        return []

    def get_block_utxos(self,block_hash):
        if block_hash in registre["block_hash"]:
            return registre["block_hash"][block_hash]
        return []

    def try_update_tree(self,transaction):
        update_success = self.update_tree(transaction)
        return update_success

    def rollback(self):
        with open("./utxo/data") as f:
            last_saved_content = f.read()
            self.load_set(last_saved_content)
    
    def save(self):

        new_set_data = {
            "arbre" : self.arbre
            "registre" : self.registre
            "current_block_hash" : self.current_block_hash
        }

        new_set_content = json.dumps(new_set_data)

        with open("./utxo/data","w") as f:
            f.write(new_set_content)
        


