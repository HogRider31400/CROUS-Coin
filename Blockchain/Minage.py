"""
    Attributs
    block qui est le bloc à miner    
    Methodes
        set_id_bloc: permet de changer de bloc à miner, on peut renseigner un set si on avait commencé à le tester
        set_set_tested: changer le set des combinaisons
        miner: mine le bloc désigné par l'attribut sur les valeurs qui ne sont pas dans le set testé.
"""
import Bloc
import json

class Minage:
    def __init__(self, bloc,id_user, set_tested=set()):
        self.bloc=bloc
        self.bloc_text = bloc.get_block_text()
        self.id_user=id_user
        self.set_tested=set_tested

    def set_id_bloc(self, new_bloc, new_set=set()):
        self.bloc=new_bloc
        self.set_tested=new_set

    def set_set_tested(self, new_set_tested):
        self.set_tested=new_set_tested

    #si on décide de faire du multi-threading c'est ici
    def miner(self):
        nonce=0
        founded=False
        while not founded:
            nonce+=1
            founded = self.test_number(nonce)
        return nonce

    def test_number(self, number):
        texte = json.loads(self.bloc_text)
        texte["pow_number"]=number
        return self.bloc.is_mined_from_text(texte)
