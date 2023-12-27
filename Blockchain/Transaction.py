"""
Classe Transaction :
Attributs :
    previous_tx_hash
    previous_tx
    id_user_giving
    id_user_getting
    amount
    date
    signature (format de la signature un tuple (r,s,px,py))

Méthodes : 
    Des getters et setter, pour le hash principalement et le reste why not
"""


class Transaction:
    
    def __init__(self):
        pass

    @classmethod
    def from_text(cls,text):
        return cls()