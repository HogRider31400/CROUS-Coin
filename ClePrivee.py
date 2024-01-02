from Point import Point
from CourbeElliptique import CourbeElliptique
import hashlib
import hmac
from Signature import Signature
import utils
class ClePrivee:

    #Attributs : e, le secret

    def __init__(self, e,G=Point(utils.generator_x,utils.generator_y,CourbeElliptique(*utils.courbe)),PREMIER=utils.prime_number,N=utils.order,h=hashlib.sha512):
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
        r = (k*G).x.nb%N
        k_inverse = pow(k, N-2, N)
        s = ((z+r*self.e)*k_inverse) % N
        if s > N/2:
            s = N - s
        return Signature(r, s)

    def determinerK(self, z):

        N = self.N
        G = self.G

        SIZE = N.bit_length()//8
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
        trouve = False
        while (not trouve):
            v = hmac.new(k, v, s256).digest()
            candidat = utils.get_int(v,N)
            if candidat >= 1 and candidat < self.PREMIER:
                return candidat
            k = hmac.new(k, v + b'\x00', s256).digest()
            v = hmac.new(k, v, s256).digest()

signature_pour_diane = ClePrivee(3)
print(signature_pour_diane.point.get_coords())
msg_zh = hashlib.sha512('3456789.232323#30#Bob'.encode('utf-8')).digest()
z= utils.get_int(msg_zh,utils.order)
print(signature_pour_diane.signer(z).get_sig())
