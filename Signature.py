class Signature:

    #Attributs : r, l'abscisse de R et s

    def __init__(self, r, s):
        self.r = r
        self.s = s

    def __repr__(self):
        return "Signature ("+str(self.r)+", "+str(self.s)+')'

    def get_sig(self):
        return (self.r,self.s)

    def verifier(self,z,G,N,P):
        s_inverse = pow(self.s,N-2,N)
        u = z*s_inverse%N
        v = self.r*s_inverse%N
        R = u*G + v*P
        return R.x.nb == self.r
