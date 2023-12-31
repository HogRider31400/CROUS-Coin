"""
    Attributs
    block qui est le bloc à miner    
    Methodes
        set_id_bloc: permet de changer de bloc à miner, on peut renseigner un set si on avait commencé à le tester
        set_set_tested: changer le set des combinaisons
        miner: mine le bloc désigné par l'attribut sur les valeurs qui ne sont pas dans le set testé.
"""


class Minage:
    def __init__(self, id_bloc,id_user, set_tested=set()):
        self.id_bloc=id_bloc
        self.id_user=id_user
        self.set_tested=set_tested

    def set_id_bloc(self, new_id_bloc, new_set=set()):
        self.id_bloc=new_id_bloc
        self.set_tested=new_set

    def set_set_tested(self, new_set_tested):
        self.set_tested=new_set_tested

    def miner(self):
        pass

    def test_number(self, number):
        pass