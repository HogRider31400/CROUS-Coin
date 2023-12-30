"""
    Attributs
    block qui est le bloc à miner    
    Methodes
        miner: prend en param un bloc, un utilisateur et un set des combinaisons déjà testée
"""


class Minage:
    def __init__(self, id_bloc,id_user, set_tested):
        self.id_bloc=id_bloc
        self.id_user=id_user
        self.set_tested=set_tested