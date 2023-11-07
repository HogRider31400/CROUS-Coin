from CorpsFini import CorpsFini
import unittest

import CorpsFini

class testCorpsFini(unittest.TestCase):

    def setUp(self):
        self.CF0=CorpsFini(0,7)
        self.CF1=CorpsFini(3,7)
        self.CF2=CorpsFini(5,7)
        self.CF3=CorpsFini(1,5)

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

    def testTrueDiv(self):
        assertEqual(self.CF1/self.CF2, CorpsFini(3*5**(5),7))
        with self.assertRaises(TypeError):
            self.CF1/self.CF3
        with self.assertRaises(ZeroDivisionError):
            self.CF1/self.CFO

    def testPow(self):
        self.assertEqual(self.CF1**0,CorpsFini(1,7))
        self.assertEqual(self.CF1**1,self.CF1)
        self.assertEqual(self.CF1*self.CF1,self.CF1**2)
        self.assertEqual(self.CF2**3, CorpsFini((5**3)%7,7))


