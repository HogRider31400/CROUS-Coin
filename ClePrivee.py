from random import randint
from Point import Point
from CourbeElliptique import CourbeElliptique
class ClePrivee:
    ###### à mettre chez le corps fini comme variable globales
    PREMIER = 512
    G = Point(15,86,CourbeElliptique(0,7,223)) #A définir
    N = G.ordre_point() #A definir, ordre du point dans la courbe
    print(N)
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
        k = self.determinerK(z)
        r = (k*G).x.nb
        k_inverse = pow(k, PREMIER-2, PREMIER)
        s = ((z+r*self.e)*k_inverse) % PREMIER
        if s > PREMIER/2:
            s = PREMIER - s
        return Signature(r, s)
  
    def determinerK(self, z):
        k = b'\x00' * SIZE
        v = b'\x01' * SIZE
        if z > PREMIER:
            z -= PREMIER
        z_bytes = z.to_bytes(SIZE, 'big')
        e_bytes = self.e.to_bytes(SIZE, 'big')
        s256 = hashlib.sha256
        #double hash sha256 pour obtenir un k,v aléatoire
        k = hmac.new(k, v + b'\x00' + e_bytes + z_bytes, s256).digest()
        v = hmac.new(k, v, s256).digest()
        k = hmac.new(k, v + b'\x01' + e_bytes + z_bytes, s256).digest()
        v = hmac.new(k, v, s256).digest()
        while True:
            v = hmac.new(k, v, s256).digest()
            candidat = int.from_bytes(v, 'big')
            if candidat >= 1 and candidat < PREMIER:
                return candidat
            k = hmac.new(k, v + b'\x00', s256).digest()
            v = hmac.new(k, v, s256).digest()


