from Point import Point
from CourbeElliptique import CourbeElliptique
import hashlib
import hmac

class ClePrivee:
    ###### à mettre chez le corps fini comme variable globales
    PREMIER = 512
    G = Point(15,86,CourbeElliptique(0,7,223))
    N = G.ordre_point()
    #Attributs : e, le secret

    def __init__(self, e):
        self.e = e
        self.point = e * G ##P = eG

    def hex(self):
        return e.zfill(64)

    def signer(self, z):
        k = self.determinerK(z)
        r = (k*G).x.nb
        k_inverse = pow(k, N-2, N)
        s = ((z+r*self.e)*k_inverse) % N
        if s > N/2:
            s = N - s
        return Signature(r, s)

    def determinerK(self, z):
        k = b'\x00' * SIZE
        v = b'\x01' * SIZE
        if z > N:
            z -= N
        z_bytes = z.to_bytes(SIZE, 'big')
        e_bytes = self.e.to_bytes(SIZE, 'big')
        s256 = hashlib.sha256
        #double hash sha256 pour limiter la collision
        k = hmac.new(k, v + b'\x00' + e_bytes + z_bytes, s256).digest()
        v = hmac.new(k, v, s256).digest()
        k = hmac.new(k, v + b'\x01' + e_bytes + z_bytes, s256).digest()
        v = hmac.new(k, v, s256).digest()
        trouve = False
        while (not trouve):
            v = hmac.new(k, v, s256).digest()
            candidat = int.from_bytes(v, 'big')
            if candidat >= 1 and candidat < N:
                trouve = True
            k = hmac.new(k, v + b'\x00', s256).digest()
            v = hmac.new(k, v, s256).digest()
        return candidat