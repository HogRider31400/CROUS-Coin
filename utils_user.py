import os
import base64
import hashlib
def dossier_existe(chemin_dossier):
    return os.path.exists(chemin_dossier) and os.path.isdir(chemin_dossier)

def hash_sha256(texte):

        return hashlib.sha256(texte.encode('utf-8')).hexdigest()