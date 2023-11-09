from CourbeElliptique import CourbeElliptique
from Point import Point
import unittest
class testPoint(unittest.TestCase):

    def setUp(self):
        self.CE = CourbeElliptique(0,7,223)
        self.CE2 = CourbeElliptique(1,0,13)
        self.CE3 = CourbeElliptique(1,0,31)

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


    def testOrdrePoint(self):
        P1 = Point(15,86,self.CE)
        P2 = Point(8,0,self.CE2)
        P3 = Point(10,3,self.CE2)
        P4 = Point(9,7,self.CE2)
        P5 = Point(26,26,self.CE3)
        P6 = Point(2,14,self.CE3)
        P7 = Point(28,1,self.CE3)

        self.assertTrue(P1.ordre_point() == 7)
        self.assertTrue(P2.ordre_point() == 2)
        self.assertTrue(P3.ordre_point() == 10)
        self.assertTrue(P4.ordre_point() == 5)
        self.assertTrue(P5.ordre_point() == 32)
        self.assertTrue(P6.ordre_point() == 8)
        self.assertTrue(P7.ordre_point() == 16)