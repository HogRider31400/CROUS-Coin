from CourbeElliptique import CourbeElliptique
from Point import Point
import unittest

class testPoint(unittest.TestCase):

    def setUp(self):
        self.CE = CourbeElliptique(0,7,223)

    def testAdd(self):
        P1 = Point(170,142,self.CE)
        P2 = Point(60,139,self.CE)
        P3 = Point(47,71,self.CE)
        P4 = Point(17,56,self.CE)
        P5 = Point(143,98,self.CE)
        P6 = Point(76,66,self.CE)

        R1 = Point(220,181,self.CE)
        R2 = Point(215,68,self.CE)
        R3 = Point(47,71,self.CE)

        self.assertTrue(P1+P2 == R1)
        self.assertTrue(P3+P4 == R2)
        self.assertTrue(P5+P6 == R3)

    def testRmul(self):
        P1 = Point(192,105,self.CE)
        P2 = Point(143,98,self.CE)
        P3 = Point(47,71,self.CE)

        R1 = Point(49,71,self.CE)
        R2 = Point(64,168,self.CE)
        R3 = Point(36,111,self.CE)
        R4 = Point(194,51,self.CE)
        R5 = Point(116,55,self.CE)

        self.assertTrue(2*P1,R1)
        self.assertTrue(2*P2,R2)
        self.assertTrue(2*P3,R3)
        self.assertTrue(4*P3,R4)
        self.assertTrue(8*P3,R5)
        self.assertTrue(21*P3,R1.id)
        with self.assertRaises(TypeError):
            P1*2



