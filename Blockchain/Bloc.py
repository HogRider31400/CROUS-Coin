"""
Classe Bloc :
Attributs
    previous_block_hash (donné à la création de l'objet)
    previous_block (retrouvé plus tard, possiblement pendant la création de l'objet)
    transactions : liste de transactions
    magic_number (si None alors le bloc n'a pas encore été miné)
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

class Bloc:
    def __init__(self):
        pass

    @classmethod
    def from_text(cls,text):
        return cls()