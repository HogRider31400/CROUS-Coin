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



