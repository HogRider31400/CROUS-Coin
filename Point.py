
class Point:
    
    #potentiellement remplacer a et b par la courbe elliptique
    def __init__(self,x,y,a,b):
        self.a = a
        self.b = b
        self.x = x
        self.y = y

        if self.x is None and self.y is None:
            return
        self.id = Point(None,None,a,b)

        #vérifier que (x,y) est sur la courbe
        if y**2!=x**3+a*x+b:
            raise ValueError("le point n'est pas sur la courbe.")
    
    def __eq__(self,other):
        return self.x == other.x and self.y == other.y and self.a == other.a and self.b == other.b

    def __add__(self,other_point):


        #1er cas l'un des deux est l'identité
        if self.x is None:
            return other_point
        if other_point.x is None:
            return self

        #2eme cas ils sont inverses
        if self.x == other_point.x and self.y == -1*other_point.y:
            return self.id
        
        #3eme cas les points ne sont pas égaux
        if self.x != other_point.x:
            slope = (other_point.y - self.y)/(other_point.x-self.x)
            new_x = slope**2 - self.x - other_point.x
            new_y = slope*(self.x-new_x) - other_point.y
            return Point(new_x,new_y,self.a,self.b)
        
        #4eme cas les points sont égaux et la slope est en +inf
        if self==other_point and self.y == 0*self.x:
            return self.id
        
        #5eme cas les points sont égaux mais y'a une slope
        if self==other_point:
            
            slope = (3*self.x**2 + self.a)/(2*self.y)
            new_x = slope**2 - 2*self.x
            new_y = slope*(self.x-new_x) - self.y
            return Point(new_x,new_y,self.a,self.b)
    
    def __mul__(self,scalaire):
        resultat = Point(None,None,self.a,self.b)
        for i in range(scalaire):
            resultat += self
        return resultat