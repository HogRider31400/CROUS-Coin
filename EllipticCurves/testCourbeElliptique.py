from CourbeElliptique import CourbeElliptique
from Point import Point
import unittest

class testCourbeElliptique(unittest.TestCase):

    def setUp(self):
        self.CE = CourbeElliptique(0,7,223)

    def testRepr(self):
        self.assertTrue(self.CE.on_curve(Point(192,105,self.CE)))
        self.assertTrue(self.CE.on_curve(Point(17,56,self.CE)))
        with self.assertRaises(ValueError) as cm:
            self.CE.on_curve(Point(200,119,self.CE))
        self.assertTrue(self.CE.on_curve(Point(1,193,self.CE)))
        with self.assertRaises(ValueError) as cm:
            self.CE.on_curve(Point(42,99,self.CE))



