from CorpsFini import CorpsFini

class CourbeElliptique:

    def __init__(self,a,b,nb_premier):
        if not type(a) is CorpsFini:
            self.a = CorpsFini(a,nb_premier)
        else:
            self.a = a
        if not type(b) is CorpsFini:
            self.b = CorpsFini(b,nb_premier)
        else:
            self.b = b
        self.nb_premier = nb_premier
    
    def __repr__(self):
        return str((self.a,self.b,self.nb_premier))
    def __eq__(self,other):
        return self.a==other.a and self.b == other.b and self.nb_premier==other.nb_premier
    def on_curve(self,point):
        return point.y**2==point.x**3+self.a*point.x+self.b