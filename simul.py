
import threading 
from Utilisateur import Utilisateur
import time
threads = []
nb_launched = 0

NB_USERS = 5

class user(threading.Thread): 
    def __init__(self, private_key): 
        threading.Thread.__init__(self) 
        self.private_key = private_key 
        self.utilisateur = Utilisateur(private_key,False)
 
        
        self.doit_update = False
        self.doit_stop = False

    def run(self): 
        print(str(self.private_key) +" est démarré")
        while nb_launched != NB_USERS:
            pass
        
        while not self.doit_stop:
            self.utilisateur.miner()
            if not self.doit_update:
                print(str(self.private_key) + " a miné un bloc et est le premier")
                for elem in threads:
                    if elem.private_key != self.private_key:
                        elem.est_derriere()
            else:
                #if not self.utilisateur.mineur.is_obsolete:
                #print(str(self.private_key) + " a miné un bloc mais n'est pas le premier")
                self.utilisateur.update_blockchain()
                self.doit_update = False
    def est_derriere(self):
        print(str(self.private_key) + " est derrière il doit se mettre à jour")
        self.doit_update = True
        self.utilisateur.mineur.is_obsolete = True

threads = []    

for i in range(NB_USERS):
    threads.append(user(2+i))

for thread in threads:
    thread.start()
    nb_launched+=1

time.sleep(100)
for thread in threads:
    thread.doit_stop = True