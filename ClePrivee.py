from Point import Point
from CourbeElliptique import CourbeElliptique
import hashlib
import hmac
from Signature import Signature

class ClePrivee:

    #Attributs : e, le secret

    def __init__(self, e,G=Point(15,86,CourbeElliptique(0,7,223)),PREMIER=512,N=7,h=hashlib.sha256):
        self.G=G
        self.PREMIER = PREMIER
        self.N = N
        self.e = e
        self.h = h
        self.point = e * G ##P = eG

    def hex(self):
        return e.zfill(64)

    def signer(self, z):

        #Coucou Diane c Alex qui a ajouté ça, à toid e le suppr
        N = self.N
        G = self.G

        k = self.determinerK(z)
        r = (k*G).x.nb
        k_inverse = pow(k, N-2, N)
        s = ((z+r*self.e)*k_inverse) % N
        if s > N/2:
            s = N - s
        return Signature(r, s)

    def determinerK(self, z):

        N = self.N
        G = self.G

        SIZE = 24
        k = b'\x00' * SIZE
        v = b'\x01' * SIZE
        if z > N:
            z -= N
        z_bytes = z.to_bytes(SIZE, 'big')
        e_bytes = self.e.to_bytes(SIZE, 'big')
        s256 = self.h
        #double hash sha256 pour obtenir un k,v aléatoire
        k = hmac.new(k, v + b'\x00' + e_bytes + z_bytes, s256).digest()
        v = hmac.new(k, v, s256).digest()
        k = hmac.new(k, v + b'\x01' + e_bytes + z_bytes, s256).digest()
        v = hmac.new(k, v, s256).digest()
        while True:
            v = hmac.new(k, v, s256).digest()
            if(len(v) > SIZE):
                v = v[(SIZE-1):]
            candidat = int.from_bytes(v)
            if candidat >= 1 and candidat < self.PREMIER:
                return candidat
            k = hmac.new(k, v + b'\x00', s256).digest()
            v = hmac.new(k, v, s256).digest()