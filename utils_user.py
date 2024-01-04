import os
import json
import base64
import hashlib
def dossier_existe(chemin_dossier):
    return os.path.exists(chemin_dossier) and os.path.isdir(chemin_dossier)

def hash_sha256(texte):
        return hashlib.sha256(texte.encode('utf-8')).hexdigest()

def get_chain_length(graphe,cur = None):

    max_l = 0 #On compte pas le cur comme faisant partie de la chaine
    for enfant in elem[cur]:
        max_l = max(max_l,get_chain_length(graphe,enfant))
    
    return max_l + 1 #Mais on le compte ici

def nb_transac_dernier_bloc(user,blocs_pas_dans):

    #On récup l'utxoset de l'user
    try:
        with open("./Users/"+user+"/utxo/data") as f:
            set_content = f.read()
        set_data = json.loads(set_content)
    except:
        return 0
    
    cur_bloc = set_data["current_block_hash"]

    for bloc in blocs_pas_dans:
        if bloc[0] == cur_bloc:
            return len(bloc[1]["transactions"])
    return 0

