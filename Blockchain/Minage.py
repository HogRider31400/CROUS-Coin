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
import hashlib

COUT = 10

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

    def maj_bloc_text(self):
        self.bloc_text = self.bloc.get_block_text()

    def setup(self):
        self.bloc.set_coinbase_transaction(COUT, self.id_user)
        self.bloc.maj_transactions()
        self.maj_bloc_text()

    #si on décide de faire du multi-threading c'est ici
    def miner(self):
        magic_nb=0
        founded=False
        self.setup()

        #A partir de maintenant on ne touche plus qu'au texte
        #pour trouver le nombre magique
        while not founded:
            magic_nb+=1
            founded = self.test_number(magic_nb)
        
        #On repasse sur l'instance du bloc
        self.fill_bloc(magic_nb)
        self.bloc.set_timestamp()
    
    def fill_bloc(self, number):
        self.bloc.set_pow_number(number)

    def test_number(self, number):
        h=hashlib.sha256()
        texte = json.loads(self.bloc_text)
        texte["pow_number"]=number
        h.update(texte.encode())
        hashed = h.hexdigest()
        target = self.bloc.get_size_target()
        return str(hashed)[0:target]=="0"*target
        
    
    
