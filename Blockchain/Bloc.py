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
import Transaction
import UTXOSet

SIZE = 32
SIZE_TARGET = 3
NB_MAX_TRANSACTIONS = 5

class Bloc:

    #static
    UTXO = UTXOSet("")

    def __init__(self, previous_block, transactions, coinbase_transaction=None, timestamp=None, pow_number=None):
        self.previous_block=previous_block
        self.transactions=transactions
        self.timestamp = timestamp
        self.pow_number = pow_number
        self.coinbase_transaction = coinbase_transaction
        
    def get_block_hash(self):
        h=hashlib.sha256()
        if self.pow_number==None:
            return -1
        h.update(self.get_block_text().to_bytes(SIZE, "big"))
        return h.digest()

    def set_pow_number(self, new_pow_number):
        self.pow_number=new_pow_number

    def is_mined(self):
        hashed = self.get_block_hash()
        return hashed>=0 and hashed[0:SIZE_TARGET]==[0]*SIZE_TARGET
    
    @staticmethod
    def is_mined_from_text(texte):
        h=hashlib.sha256()
        h.update(texte.to_bytes(SIZE, "big"))
        hashed = h.digest()
        return hashed[0:SIZE_TARGET]==[0]*SIZE_TARGET
    
    def add_transaction(self, transaction):
        if len(self.transactions)<NB_MAX_TRANSACTIONS and self.timestamp!=None:
            self.transactions.append(transaction)
        else:
            print("Nombre max de transactions atteint.")
    
    """
        il faut rajouter la vérification du bloc précédent.
    """
    def is_valid(self):
        self.maj_transactions()
        if not self.is_mined():
            return False
        self.timestamp = time.time()
        return True

    def maj_transactions(self):
        for transaction in self.transactions:
            if not transaction.verifier() or not self.UTXO.try_update_tree(transaction):
                self.transactions.remove(transaction)
        self.UTXO.save()

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
    
    def get_letfovers(self):
        somme=0
        for transaction in self.transactions:
            somme+=transaction.differenceIO()
        return somme
    

    #transaction sans input à faire 
    #ajouter en plus le surplus de toutes les tx
    def set_coinbase_transaction(self, value, id_mineur):
        self.coinbase_transaction = Transaction([], [], mineur.get_id())

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
            "coinbase_transaction" : self.coinbase_transaction,
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
        coinbase_transaction = bloc_data["coinbase_transaction"]
        pow_number = bloc_data["pow_number"]


        return cls(previous_block_hash,transactions,coinbase_transaction, timestamp,pow_number)