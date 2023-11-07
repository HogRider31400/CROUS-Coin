from random import randint

class ClePrivee:
    ###### à mettre chez le corps fini comme variable globale
    PREMIER = 512

    #Attributs : e, le secret

    def __init__(self, e):
        self.e = e
        self.point = e * G ##P = eG

    def hex(self):
        return e.zfill(64)

    def signer(self, z):
        ####---------------------------------------------
        ## Déterminer un meilleur moyen d'avoir k
        ###----------------------------------------------
        ######RENDRE K UNIQUE, cf la suite
        k = randint(0, 2**PREMIER)
        r = (k*G).x.nb
        k_inverse = pow(k, PREMIER-2, PREMIER)
        s = ((z+r*self.e)*k_inverse) % PREMIER
        if s > PREMIER/2:
            s = PREMIER - s
        return Signature(r, s)