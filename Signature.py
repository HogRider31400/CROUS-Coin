class Signature:

    #Attributs : r, l'abscisse de R et s

    def __init__(self, r, s):
        self.r = r
        self.s = s

    def __repr__(self):
        return "Signature ("+str(r)+", "+str(s)+')'
    
    def verifier(self,z,G,N,P):
        s_inverse = pow(self.s,-1,N)
        u = (z*s_inverse)%N
        v = (self.r*s_inverse)%N
        total = u*G + v*P
        return total.x.nb == self.r