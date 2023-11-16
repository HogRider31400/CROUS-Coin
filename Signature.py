class Signature:

    #Attributs : r, l'abscisse de R et s

    def __init__(self, r, s):
        self.r = r
        self.s = s

    def __repr__(self):
        return "Signature ("+str(r)+", "+str(s)+')'
    
    def verifier(self,z,G,N,P):
        s_inverse = pow(self.s,N-2,N)
        u = z*s_inverse%N
        v = self.r*s_inverse%N
        total = u*G + v*P
        return total.x.nb == self.r

from CourbeElliptique import CourbeElliptique
from Point import Point
from CorpsFini import CorpsFini
import hashlib

CE = CourbeElliptique(0,7, 2**256 - 2**32 - 977)

G = Point(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798, 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8,CE)
N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141

P = Point(0x04519fac3d910ca7e7138f7013706f619fa8f033e6ec6e09370ea38cee6a7574,0x82b51eab8c27c66e26c858a079bcdf4f1ada34cec420cafc7eac1a42216fb6c4,CE)

s256 = hashlib.sha512

S = Signature(0x37206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c6,0x8ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec)

z = 0xbc62d4b80d9e36da29c16c5d4d9f11731f36052c72401a76c23c0fb5a9b74423 #int.from_bytes(s256('sample'.encode('utf-8')).digest(), byteorder="big")
print(S.verifier(z,G,N,P))
print(len(s256('sample'.encode('utf-8')).hexdigest()))