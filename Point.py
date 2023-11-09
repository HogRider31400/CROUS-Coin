from CorpsFini import CorpsFini
from CourbeElliptique import CourbeElliptique
class Point:
    CE = CourbeElliptique(0,7,223)
    #potentiellement remplacer a et b par la courbe elliptique
    def __init__(self,x,y,CE=None):
        if CE and self.CE != CE:
            self.CE = CE
        if not type(x) is CorpsFini:
            self.x = CorpsFini(x,self.CE.nb_premier)
        else:
            self.x = x
        if not type(y) is CorpsFini:
            self.y = CorpsFini(y,self.CE.nb_premier)
        else:
            self.y = y

        if x is None and y is None:
            return
        self.id = Point(None,None,self.CE)

        #vérifier que (x,y) est sur la courbe
        if not self.CE.on_curve(self):
            raise ValueError("le point n'est pas sur la courbe.")

    def __eq__(self,other):
        return self.x == other.x and self.y == other.y and self.CE == other.CE


    def __add__(self,other_point):


        #1er cas l'un des deux est l'identité
        if self.x.nb is None:
            return other_point
        if other_point.x.nb is None:
            return self

        #2eme cas ils sont inverses
        if self.x == other_point.x and self.y == -1*other_point.y:
            return self.id

        #3eme cas les points ne sont pas égaux
        if self.x != other_point.x:
            slope = (other_point.y - self.y)/(other_point.x-self.x)
            new_x = slope**2 - self.x - other_point.x
            new_y = slope*(self.x-new_x) - self.y
            return Point(new_x,new_y,self.CE)

        #4eme cas les points sont égaux et la slope est en +inf
        if self==other_point and self.y == 0*self.x:
            return self.id

        #5eme cas les points sont égaux mais y'a une slope
        if self==other_point:
            slope = (3*self.x**2 + self.CE.a)/(2*self.y)
            new_x = slope**2 - 2*self.x
            new_y = slope*(self.x-new_x) - self.y
            return Point(new_x,new_y,self.CE)

    def __rmul__(self,scalaire):
        resultat = Point(None,None,self.CE)
        for i in range(scalaire):
            resultat += self
        return resultat
    def ordre_point(self):
        cur_point = self
        nb = 1
        while not (cur_point == Point(None,None,self.CE)):
            cur_point += self
            nb += 1
        return nb