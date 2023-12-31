"""
Classe Bloc :
Attributs
    previous_block_hash (donné à la création de l'objet)
    timestamp : moment où le bloc est certifié valide/complet
    transactions : liste de transactions
    pow_number (si None alors le bloc n'a pas encore été miné)
Méthodes :
    is_valid
    is_mined
    get_block_hash
    get_block_text (donne le bloc sous adaptée pour le stocker)
    add_transaction: ajoute une transaction dans la limite fixée
    fill_block rempli
Constructeurs :
    Soit un qui prend le prev hash, les transactions (déjà parsés) et un nombre
    Soit il prend un fichier texte à parse dans le format du bloc
"""

import json
import hashlib
import time
import Transaction

SIZE = 32
SIZE_TARGET = 3
NB_MAX_TRANSACTIONS = 5

class Bloc:

    def __init__(self, previous_block, transactions, timestamp=None, pow_number=None):
        self.previous_block=previous_block
        self.transactions=transactions
        self.timestamp = timestamp
        self.pow_number = pow_number
        
    def get_block_hash(self):
        h=hashlib.sha256()
        if self.pow_number==None:
            return -1
        h.update(self.get_block_text().to_bytes(SIZE, "big"))
        return h.digest()

    def set_pow_number(self, new_pow_number):
        self.pow_number=new_pow_number

    def is_mined(self):
        hash = self.get_block_hash()
        return hash>=0 and hash[0:SIZE_TARGET]==[0]*SIZE_TARGET
    
    def add_transaction(self, transaction):
        if len(self.transactions)<NB_MAX_TRANSACTIONS:
            self.transactions.append(transaction)
        else:
            print("Nombre max de transactions atteint.")
    
    """
        il faut rajouter les vérifications des tx dans le utxo + la vérification du bloc précédent.
    """
    def is_valid(self):
        for transaction in self.transactions:
            if not transaction.verifier():
                return False
        if not self.is_mined():
            return False
        self.timestamp = time.time()
        return True

    def __repr__(self):
        output=""
        output.append("BLOC \n")
        output.append("Previous bloc hash: " + self.previous_block + "\n")
        output.append("Transactions: \n")
        for transaction in self.transactions:
            output.append(transaction + "\n")
        output.append("Timestamp: " + self.timestamp + "\n")
        output.append("Proof of work: " + self.pow_number + "\n")
        return output
    
    def get_letfovers(self):
        somme=0
        for transaction in self.transactions:
            somme+=transaction.differenceIO()
        return somme

    def get_block_text(self):
        
        tx_list_data = []

        for tx in self.transactions:
            tx_list_data.append(
                {
                    "horodatage" : tx.getHorodatage(),
                    "inputs" : tx.getInputs(),
                    "outputs" : tx.getOutputs()
                }
            )


        block_data = {
            "previous_block_hash" : self.previous_block,
            "timestamp" : self.timestamp,
            "transactions" : tx_list_data,
            "pow_number" : self.pow_number
        }

        return json.dumps(block_data)
    
    def save(self):

        with open("./blocs/"+self.get_block_hash(),"w") as f:
            f.write(self.get_block_text())

    @classmethod
    def from_text(cls,text):
        bloc_data = json.loads(text)

        previous_block_hash = bloc_data["previous_block_hash"]
        timestamp = bloc_data["timestamp"]
        transactions_data = bloc_data["transactions"]
        transactions = []
        for cur_trans in transactions_data:
            transactions.append(Transaction.from_text(cur_trans))
        pow_number = bloc_data["pow_number"]


        return cls(previous_block_hash,transactions,timestamp,pow_number)