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
    def __init__(self, bloc,id_user,user, set_tested=set()):
        self.bloc=bloc
        self.private_key = user.private_key
        self.user_object = user
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
        self.bloc.set_coinbase_transaction(COUT, self)
       #print("COINBASE TRANSACTION AVANT MAJ BLOC TEXT")
        #print(self.bloc.coinbase_transaction)
        #self.bloc.maj_transactions()
        self.maj_bloc_text()
        #print("COINBASE TRANSACTION APRES MAJ BLOC TEXT")
        #print(self.bloc.coinbase_transaction)

    def get_id(self):
        return self.id_user

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
        h = hashlib.sha512()
        texte = json.loads(self.bloc_text)
        texte["pow_number"] = number
        h.update(json.dumps(texte).encode())
        hashed = h.hexdigest()
        target = self.bloc.get_size_target()
        print(str(hashed))
        return str(hashed)[0:target] == "0"*target
        
    
    
