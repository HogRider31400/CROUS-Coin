import CorpsFini
import unittest

class testCorpsFini(unittest.TestCase):

    def setUp(self):
        self.CF1=CorpsFini(3,7)
        self.CF2=CorpsFini(5,7)

    def testRepr(self):
        assertEqual(repr(self.corpsFini),'(3,7)')

    def testEqual(self):
        assertFalse(self.CF1==self.CF2)
        assertTrue(self.CF1==self.CF1)

    def testAdd(self):
        assertEqual(self.CF1+self.CF2,CorpsFini(1,7))
        assertEqual(self.CF1+CorpsFini(2,7), self.CF2)

    def testSub(self):
        assertEqual(self.CF2-self.CF1,CorpsFini(2,7))
        assertEqual(self.CF1-self.CF1, CorpsFini(0,7))
    
    def testMul(self):
        assertEqual(self.CF1*self.CF2,CorpsFini(1,7))
        assertEqual(self.CF1*CorpsFini(2,7), CorpsFini(6,7))

    #TODO: test de la division 
    def testTrueDiv(self):
        pass

    def testPow(self):
        assertEqual(self.CF1**0,CorpsFini(1,7))
        assertEqual(self.CF1**1,self.CF1)
        assertEqual(self.CF1*self.CF1,self.CF1**2)
        assertEqual(self.CF2**3, CorpsFini((5**3)%7,7))






