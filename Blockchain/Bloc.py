"""
Classe Bloc :
Attributs
    previous_block_hash (donné à la création de l'objet)
    timestamp : moment où le bloc a été miné, initialisé null
    transactions : liste de transactions
    pow_number (si None alors le bloc n'a pas encore été miné)
Méthodes :
    is_valid
    is_mined
    get_block_hash
    get_block_text (donne le bloc sous adaptée pour le stocker)
    et pourquoi pas des setter et des getter autres
Constructeurs :
    Soit un qui prend le prev hash, les transactions (déjà parsés) et un nombre
    Soit il prend un fichier texte à parse dans le format du bloc
"""

import json
import hashlib

SIZE = 32
SIZE_TARGET = 3

class Bloc:

    def __init__(self, previous_block, transactions):
        self.previous_block=previous_block
        self.transactions=transactions
        self.timestamp = None
        self.pow_number = None
        
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
    
    def get_block_text(self):
        pass

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


        return cls(previous_block_hash,timestamp,transactions,pow_number)