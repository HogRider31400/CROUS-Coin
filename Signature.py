class Signature:

    #Attributs : r, l'abscisse de R et s

    def __init__(self, r, s):
        self.r = r
        self.s = s

    def __repr__(self):
        return "Signature ("+str(r)+", "+str(s)+')'