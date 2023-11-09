class Signature:

    #Attributs : r, l'abscisse de R et s

    def __init__(self, r, s):
        self.r = r
        self.s = s

    def __repr__(self):
        return "Signature ("+str(r)+", "+str(s)+')'
    
    def verifier(self,z,G,N):
        s_inverse = pow(self.s,N-2,N)
        u = z*s_inverse%N
        v = self.r*s_inv%N
        total = u*G + v*self.point
        return total.x == self.r