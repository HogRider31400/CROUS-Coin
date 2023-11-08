from random import randint
from Point import Point
def ordre_point(point):
    cur_point = point
    nb = 1
    while not (cur_point == Point(None,None,point.a,point.b,point.nb_premier)):
        print(cur_point.x,cur_point.y)
        cur_point += point
        nb += 1
    return nb

print(ordre_point(Point(15,86,0,7,223)))

class ClePrivee:
    ###### à mettre chez le corps fini comme variable globale
    PREMIER = 512
    G = (1,1) #A définir
    N = 1 #A definir, ordre du point dans la courbe

    #Attributs : e, le secret

    def __init__(self, e):
        self.e = e
        self.point = e * G ##P = eG

    def hex(self):
        return e.zfill(64)
    
    def verifier(self,z,signature):
        s_inverse = pow(signature.s,N-2,N)
        u = z*s_inverse%N
        v = signature.r*s_inv%N
        total = u*G + v*self
        return total.x == signature.r

    def signer(self, z):
        ####---------------------------------------------
        ## Déterminer un meilleur moyen d'avoir k
        ###----------------------------------------------
        ######RENDRE K UNIQUE, cf la suite
        k = randint(0, 2**N)
        r = (k*G).x.nb
        k_inverse = pow(k, N-2, N)
        s = ((z+r*self.e)*k_inverse) % N
        if s > N/2:
            s = N - s
        return Signature(r, s)