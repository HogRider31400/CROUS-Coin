from CourbeElliptique import CourbeElliptique
from Point import Point
from CorpsFini import CorpsFini
import hashlib
from Signature import Signature
from ClePrivee import ClePrivee
import unittest

class testSignature(unittest.TestCase):

    def setUp(self):
        pass

    def testCourbeLivre(self):
        CE = CourbeElliptique(0,7, 2**256 - 2**32 - 977)

        G = Point(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798, 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8,CE)
        N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141

        P = Point(0x04519fac3d910ca7e7138f7013706f619fa8f033e6ec6e09370ea38cee6a7574,0x82b51eab8c27c66e26c858a079bcdf4f1ada34cec420cafc7eac1a42216fb6c4,CE)

        s256 = hashlib.sha512

        S = Signature(0x37206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c6,0x8ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec)

        z = 0xbc62d4b80d9e36da29c16c5d4d9f11731f36052c72401a76c23c0fb5a9b74423 #int.from_bytes(s256('sample'.encode('utf-8')).digest(), byteorder="big")
        self.assertTrue(S.verifier(z,G,N,P))

    def testCourbeNIST192(self):
        CE = CourbeElliptique(0xfffffffffffffffffffffffffffffffefffffffffffffffc,0x64210519e59c80e70fa7e9ab72243049feb8deecc146b9b1,0xfffffffffffffffffffffffffffffffeffffffffffffffff)
        G = Point(0x188da80eb03090f67cbf20eb43a18800f4ff0afd82ff1012, 0x07192b95ffc8da78631011ed6b24cdd573f977a11e794811,CE)
        N = 0xffffffffffffffffffffffff99def836146bc9b1b4d22831 * 0x1

        SK = ClePrivee(0x6FAB034934E4C0FC9AE67F5B5659A9D7D1FEFD187EE09FD4,
                        G,
                        0xfffffffffffffffffffffffffffffffeffffffffffffffff,
                        N,
                        hashlib.sha256)
        P = SK.point

        s256 = hashlib.sha256

        z = int.from_bytes(s256('sample'.encode('utf-8')).digest(), byteorder="big") % N

        S = SK.signer(z)
        self.assertTrue(S.verifier(z,G,N,P))
