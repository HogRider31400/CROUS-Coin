from CorpsFini import CorpsFini
import unittest

class testCorpsFini(unittest.TestCase):

    def setUp(self):
        self.CF1=CorpsFini(3,7)
        self.CF2=CorpsFini(5,7)

    def testRepr(self):
        self.assertEqual(repr(self.corpsFini),'(3,7)')

    def testEqual(self):
        assertFalse(self.CF1==self.CF2)
        assertTrue(self.CF1==self.CF1)

    def testAdd(self):
        self.assertEqual(self.CF1+self.CF2,CorpsFini(1,7))
        self.assertEqual(self.CF1+CorpsFini(2,7), self.CF2)

    def testSub(self):
        self.assertEqual(self.CF2-self.CF1,CorpsFini(2,7))
        self.assertEqual(self.CF1-self.CF1, CorpsFini(0,7))
    
    def testMul(self):
        self.assertEqual(self.CF1*self.CF2,CorpsFini(1,7))
        self.assertEqual(self.CF1*CorpsFini(2,7), CorpsFini(6,7))

    #TODO: test de la division 
    def testTrueDiv(self):
        pass

    def testPow(self):
        self.assertEqual(self.CF1**0,CorpsFini(1,7))
        self.assertEqual(self.CF1**1,self.CF1)
        self.assertEqual(self.CF1*self.CF1,self.CF1**2)
        self.assertEqual(self.CF2**3, CorpsFini((5**3)%7,7))


if __name__ == '__main__':
        unittest.main(verbosity=2)


