"""
Classe Bloc :
Attributs
    previous_block_hash (donné à la création de l'objet)
    timestamp : moment où le bloc est certifié valide/complet
    transactions : liste de transactions
    coinbase_transaction:
    pow_number (si None alors le bloc n'a pas encore été miné)
Méthodes :
    is_valid
    is_mined
    get_block_hash
    get_block_text (donne le bloc sous adaptée pour le stocker)
    add_transaction: ajoute une transaction dans la limite fixée
Constructeurs :
    Soit un qui prend le prev hash, les transactions (déjà parsés) et un nombre
    Soit il prend un fichier texte à parse dans le format du bloc
"""
import copy
import json 
import hashlib
import time
from Transaction import Transaction

from UTXOSet import UTXOSet
import os

SIZE_TARGET = 3
NB_MAX_TRANSACTIONS = 5
INITIAL_REWARD = 20
WAVE = 100

class Bloc:

    hauteur=0

    def __init__(self, previous_block_hash, transactions, coinbase_transaction=None, timestamp=None, pow_number=None,BLOC_FOLDER='./blocs',utxo_set=""):
        self.utxo_set = utxo_set 
        self.BLOC_FOLDER = BLOC_FOLDER
        self.previous_block_hash=previous_block_hash
        self.transactions=transactions
        self.timestamp = timestamp
        self.pow_number = pow_number
        self.set_hauter()
        self.reward = self._set_reward()
        self.coinbase_transaction = coinbase_transaction

    @classmethod
    def from_text(cls,text,BLOC_FOLDER='./blocs',utxo_set=""):
        bloc_data = json.loads(text)

        previous_block_hash = bloc_data["previous_block_hash"]
        timestamp = bloc_data["timestamp"]
        transactions_data = bloc_data["transactions"]
        transactions = []
        for cur_trans in transactions_data:
            transactions.append(Transaction.from_text(cur_trans,utxo_set))
        if bloc_data["coinbase_transaction"] != None:
            coinbase_transaction = Transaction.from_text(bloc_data["coinbase_transaction"],utxo_set)
        else:
            coinbase_transaction = None
        pow_number = bloc_data["pow_number"]


        return cls(previous_block_hash,transactions,coinbase_transaction, timestamp,pow_number,BLOC_FOLDER,utxo_set)

    
        

    #-----------------------------------------------------------#
    #------------------------- Getters -------------------------#
    #-----------------------------------------------------------#
        
    def get_block_hash(self):
        
        if self.pow_number==None:
            return -1
        h = hashlib.sha256(self.get_block_text_for_hash().encode())
        return h.hexdigest()
    
    def get_pow_number(self):
        return self.pow_number
    
    def get_leftovers(self):
        somme=0
        for transaction in self.transactions:
            somme+=transaction.differenceIO()
        return somme
    
    def get_previous_bloc_hash(self):
        return self.previous_block_hash

    def get_transactions(self):
        return self.transactions
    
    def get_coinbase_transaction(self):
        return self.coinbase_transaction
    
    @staticmethod
    def get_size_target():
        return SIZE_TARGET
    
    def get_reward(self):
        print("reward : " + self.reward)
        return self.reward
    
    def get_dict(self):
        
        #fonction qui met les transactions sous forme de texte.
        def get_tx_data(tx):
            if tx == None:
                return None
            inputs = []
            for cur_input in copy.deepcopy(tx.get_inputs()):
                new_input = cur_input 
                new_input["cleAcheteur"] = tuple(cur_input["cleAcheteur"].get_coords())
                new_input["sigAcheteur"] = tuple(cur_input["sigAcheteur"].get_sig())
                inputs.append(new_input)

            outputs = []

            for cur_output in copy.deepcopy(tx.get_outputs()):
                new_output = cur_output
                new_output["cleVendeur"] = tuple(cur_output["cleVendeur"].get_coords())
                new_output["sigVendeur"] = tuple(cur_output["sigVendeur"].get_sig())
                outputs.append(new_output)
            
            return {
                    "horodatage" : tx.get_horodatage(),
                    "acheteur" : tx.adresseAcheteur,
                    "inputs" : inputs,
                    "outputs" : outputs
                }
        coinbase_transaction = get_tx_data(self.coinbase_transaction)        

        tx_list_data = []
 
        for tx in self.transactions:
            tx_list_data.append(
                get_tx_data(tx)
            )


        bloc_data = {
            "previous_block_hash" : self.previous_block_hash,
            "timestamp" : self.timestamp,
            "coinbase_transaction" : coinbase_transaction,
            "transactions" : tx_list_data,
            "pow_number" : self.pow_number
        }

        return bloc_data

    #-----------------------------------------------------------#
    #------------------------- Setters -------------------------#
    #-----------------------------------------------------------#

    def set_pow_number(self, new_pow_number):
        if self.is_finished():
            print("Erreur: bloc fermé, plus de modifications possibles")
            return
        self.pow_number=new_pow_number

    def set_coinbase_transaction(self, mineur):
        #print("Je passe dans set_coinbasetx")
        if self.is_finished():
            print("Erreur: bloc fermé, plus de modifications possibles")
            return
        self.coinbase_transaction = Transaction([],[],mineur.get_id(),None,self.utxo_set)
        montant = self.reward + self.get_leftovers()
        msg = self.coinbase_transaction.hasher_msg(self.coinbase_transaction.creer_msg(self.coinbase_transaction.get_horodatage(), montant, mineur.get_id()))
        #print(self.coinbase_transaction.creer_msg(self.coinbase_transaction.get_horodatage(), montant, mineur.get_id()))
        output = self.coinbase_transaction.creer_une_output_dico(mineur.get_id(), montant , mineur.private_key.signer(msg), mineur.private_key.point)
        #print("SALUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUT")
        #print(output)
        self.coinbase_transaction.ajouter_outputs([output])


    #methode qui permet de sceller le bloc
    def set_timestamp(self):
        if self.is_finished():
            print("Erreur: bloc fermé, plus de modifications possibles")
            return
        if self.is_valid():
            Bloc.hauteur+=1
            self.timestamp = time.time()

    def _set_reward(self):
        return INITIAL_REWARD * (1/2) ** (self.hauteur // WAVE)
    
    def set_hauter(self):
        Bloc.hauteur = self.utxo_set.get_hauteur()

    #-----------------------------------------------------------#
    #-------------------------- State --------------------------#
    #-----------------------------------------------------------#
    
    def is_finished(self):
        return self.timestamp!=None

    def is_mined(self):
        hashed = self.get_block_hash()
        print(hashed)
        return hashed!=-1 and str(hashed)[0:SIZE_TARGET]=="0"*SIZE_TARGET
    
    def is_full(self):
        return len(self.transactions)==NB_MAX_TRANSACTIONS
    
    """
        il faut rajouter la vérification du bloc précédent.
    """
    def is_valid(self):
        if not self.transactions_valid():
            print("Non valide: transactions invalides.")
            return False 
        if not self.coinbase_transaction.verifier_coinBase_transaction():
            print("Non valide: coinbase transaction pas valide.")
        if not self.is_mined():
            print("Non valide: bloc pas miné.")
            return False
        if not self.previous_bloc_is_founded():
            print("Non valide: precedent bloc pas trouvé.")
            return False
        return True

    def transactions_valid(self):
        for transaction in self.transactions:
            #print(transaction.verifier())
            if not transaction.verifier(): # or not self.utxo_set.try_update_tree(transaction):
                return False
        return True
    
    def previous_bloc_is_founded(self):
        if self.previous_block_hash == None:
            return True
        for b in os.listdir(self.BLOC_FOLDER):
            if b == self.previous_block_hash:
                return True
        return False
    
    #-----------------------------------------------------------#
    #------------------------- Others --------------------------#
    #-----------------------------------------------------------#
    
    
    def maj_transactions(self):
        if self.is_finished():
            print("Erreur: bloc fermé, plus de modifications possibles")
            return 
        for transaction in self.transactions:
            if not transaction.verifier() or not self.UTXO.try_update_tree(transaction):
                self.transactions.remove(transaction)
        self.UTXO.save()
    
    def add_transaction(self, transaction):
        if self.is_finished():
            print("Erreur: bloc fermé, plus de modifications possibles")
            return
        if len(self.transactions)<NB_MAX_TRANSACTIONS and self.timestamp!=None:
            self.transactions.append(transaction)
        else:
            print("Nombre max de transactions atteint.")

    
    #-----------------------------------------------------------#
    #------------------------- Saving --------------------------#
    #-----------------------------------------------------------#

    #méthode utilisée pour la sauvegarde 
    def get_block_text(self):
        bloc_data = self.get_dict()
        return json.dumps(bloc_data)
    
    #méthode utilisée pour hasher, en eleve le timestamp
    def get_block_text_for_hash(self):
        bloc_data = self.get_dict()
        del bloc_data['timestamp']
        return json.dumps(bloc_data)
    
    def save(self):
        if self.is_finished():
            path = self.BLOC_FOLDER+self.get_block_hash()
            with open(path,"w") as f:
                f.write(self.get_block_text())
    