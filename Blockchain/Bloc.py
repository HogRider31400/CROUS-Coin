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

import json 
import hashlib
import time
from Transaction import Transaction
from Utilisateur import Utilisateur
from UTXOSet import UTXOSet

SIZE = 32
SIZE_TARGET = 1
NB_MAX_TRANSACTIONS = 5

class Bloc:

    def __init__(self, previous_block_hash, transactions, coinbase_transaction=None, timestamp=None, pow_number=None,BLOC_FOLDER='./blocs',utxo_set=""):
        self.utxo_set = utxo_set 
        self.BLOC_FOLDER = BLOC_FOLDER
        self.previous_block_hash=previous_block_hash
        self.transactions=transactions
        self.timestamp = timestamp
        self.pow_number = pow_number
        self.coinbase_transaction = coinbase_transaction

    @classmethod
    def from_text(cls,text,BLOC_FOLDER='./blocs',utxo_set=""):
        bloc_data = json.loads(text)

        previous_block_hash = bloc_data["previous_block_hash"]
        timestamp = bloc_data["timestamp"]
        transactions_data = bloc_data["transactions"]
        transactions = []
        for cur_trans in transactions_data:
            transactions.append(Transaction.from_text(cur_trans))
        coinbase_transaction = Transaction.from_text(bloc_data["coinbase_transaction"])
        pow_number = bloc_data["pow_number"]


        return cls(previous_block_hash,transactions,coinbase_transaction, timestamp,pow_number,BLOC_FOLDER,utxo_set)

    #-----------------------------------------------------------#
    #------------------------- Getters -------------------------#
    #-----------------------------------------------------------#
        
    def get_block_hash(self):
        h=hashlib.sha256()
        if self.pow_number==None:
            return -1
        h.update(self.get_block_text().encode())
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
    
    @staticmethod
    def get_size_target():
        return SIZE_TARGET
    
    #-----------------------------------------------------------#
    #------------------------- Setters -------------------------#
    #-----------------------------------------------------------#

    def set_pow_number(self, new_pow_number):
        if self.is_finished():
            print("Erreur: bloc fermé, plus de modifications possibles")
            return
        self.pow_number=new_pow_number

    #transaction sans input à faire 
    #ajouter en plus le surplus de toutes les tx
    def set_coinbase_transaction(self, value, mineur):
        if self.is_finished():
            print("Erreur: bloc fermé, plus de modifications possibles")
            return
        self.coinbase_transaction = Transaction([],[],mineur.get_id())
        montant = value+self.get_leftovers()
        msg = self.coinbase_transaction.hasher_msg(self.coinbase_transaction.creer_msg(self.coinbase_transaction.get_horodatage(), montant, mineur.get_id()))
        output = self.coinbase_transaction.creer_une_output_dico(mineur, montant , mineur.private_key.signer(msg), mineur.private_key.point)
        self.coinbase_transaction.ajouter_outputs([output])


    #methode qui permet de sceller le bloc
    def set_timestamp(self):
        if self.is_finished():
            print("Erreur: bloc fermé, plus de modifications possibles")
            return
        if self.is_valid():
            self.timestamp = time.time()

    #-----------------------------------------------------------#
    #-------------------------- State --------------------------#
    #-----------------------------------------------------------#
    
    def is_finished(self):
        return self.timestamp!=None

    def is_mined(self):
        hashed = self.get_block_hash()
        return hashed!=-1 and str(hashed)[0:SIZE_TARGET]=="0"*SIZE_TARGET
    
    """
        il faut rajouter la vérification du bloc précédent.
    """
    def is_valid(self):
        self.transactions_valid()
        if not self.is_mined():
            return False
        return True

    def transactions_valid(self):
        for transaction in self.transactions:
            if not transaction.verifier() or not self.UTXO.try_update_tree(transaction):
                return False
        return True
    
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

    def __repr__(self):
        output=""
        output.append("BLOC \n")
        output.append("Previous bloc hash: " + self.previous_block + "\n")
        output.append("Coinbase transactoin: " + self.coinbase_transaction + "\n")
        output.append("Transactions: \n")
        for transaction in self.transactions:
            output.append(transaction + "\n")
        output.append("Timestamp: " + self.timestamp + "\n")
        output.append("Proof of work: " + self.pow_number + "\n")
        return output
    
    
    
    #-----------------------------------------------------------#
    #------------------------- Saving --------------------------#
    #-----------------------------------------------------------#
    

    def get_block_text(self):
        
        def get_tx_data(tx):
            if tx == None:
                return None
            inputs = []
            for cur_input in tx.get_inputs():
                new_input = cur_input 
                new_input["cleAcheteur"] = cur_input["cleAcheteur"].get_coords()
                new_input["sigAcheteur"] = cur_input["sigAcheteur"].get_sig()
                inputs.append(new_input)

            outputs = []

            for cur_output in tx.get_outputs():
                new_output = cur_output
                new_output["cleVendeur"] = cur_output["cleVendeur"].get_coords()
                new_output["sigVendeur"] = cur_output["sigVendeur"].get_sig()
                outputs.append(new_output)
            
            return {
                    "horodatage" : tx.get_horodatage(),
                    "inputs" : inputs,
                    "outputs" : outputs
                }


        coinbase_transaction = get_tx_data(self.coinbase_transaction)        

        tx_list_data = []
 
        for tx in self.transactions:
            tx_list_data.append(
                get_tx_data(tx)
            )


        block_data = {
            "previous_block_hash" : self.previous_block_hash,
            "timestamp" : self.timestamp,
            "coinbase_transaction" : coinbase_transaction,
            "transactions" : tx_list_data,
            "pow_number" : self.pow_number
        }

        return json.dumps(block_data)
    
    def save(self):

        with open(self.UTXO_FOLDER+self.get_block_hash(),"w") as f:
            f.write(self.get_block_text())

    