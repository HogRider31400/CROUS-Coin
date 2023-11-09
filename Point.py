import CorpsFini

class Point:
    
    #potentiellement remplacer a et b par la courbe elliptique
    def __init__(self,x,y,a,b,nb_premier):
        if not type(a) is CorpsFini.CorpsFini:
            self.a = CorpsFini.CorpsFini(a,nb_premier)
        else:
            self.a = a
        if not type(b) is CorpsFini.CorpsFini:
            self.b = CorpsFini.CorpsFini(b,nb_premier)
        else:
            self.b = b
        self.nb_premier = nb_premier
        if not type(x) is CorpsFini.CorpsFini:
            self.x = CorpsFini.CorpsFini(x,nb_premier)
        else:
            self.x = x
        if not type(y) is CorpsFini.CorpsFini:
            self.y = CorpsFini.CorpsFini(y,nb_premier)
        else:
            self.y = y

        if x is None and y is None:
            return
        self.id = Point(None,None,a,b,self.nb_premier)

        #vérifier que (x,y) est sur la courbe
        if self.y**2!=self.x**3+self.a*self.x+self.b:
            raise ValueError("le point n'est pas sur la courbe.")
    
    def __eq__(self,other):
        return self.x == other.x and self.y == other.y and self.a == other.a and self.b == other.b


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
            return Point(new_x,new_y,self.a.nb,self.b.nb,self.nb_premier)
        
        #4eme cas les points sont égaux et la slope est en +inf
        if self==other_point and self.y == 0*self.x:
            return self.id
        
        #5eme cas les points sont égaux mais y'a une slope
        if self==other_point:
            slope = (3*self.x**2 + self.a)/(2*self.y)
            new_x = slope**2 - 2*self.x
            new_y = slope*(self.x-new_x) - self.y
            return Point(new_x,new_y,self.a.nb,self.b.nb,self.nb_premier)
    
    def __rmul__(self,scalaire):
        resultat = Point(None,None,self.a.nb,self.b.nb,self.nb_premier)
        for i in range(scalaire):
            resultat += self
        return resultat