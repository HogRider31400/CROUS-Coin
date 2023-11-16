from Point import Point
from CourbeElliptique import CourbeElliptique
from random import randint
import subprocess
def ordre_courbe(CE):

    SageCE = subprocess.run('sage -c "print(EllipticCurve(GF('+str(CE.nb_premier)+'),['+str(CE.a.nb)+','+str(CE.b.nb)+']).cardinality(algorithm=\'pari\'))"',capture_output=True,shell=True)
    return int(SageCE.stdout)

def aBonK(CE,ordre_CE):
    k = 1
    while (CE.nb_premier**k - 1) % ordre_CE != 0:
        if k >= 12:
            return True
        k += 1
    print("On a trouvé K pour",CE,"c'est",k)
    if k >= 12:
        return True
    return False

def recup_generateur(CE):
    SageCE = subprocess.run('sage -c "print(EllipticCurve(GF('+str(CE.nb_premier)+'),['+str(CE.a.nb)+','+str(CE.b.nb)+']).gens()[0])"',capture_output=True,shell=True)
    sansParens = str(SageCE.stdout[1:-2])
    pointStr = sansParens.split(":")[0:2]
    return Point(int(str(pointStr[0])[2:]),int(str(pointStr[1])),CE)

premiers = [2**512+75,2**512-569,2**512-2**511+111]


def generate_random_curves(nb,prime):
    curves = []
    for i in range(nb):
        curves.append(CourbeElliptique(randint(0,500),randint(0,500),prime))
    return curves

for prime in premiers:
    print("Premier actuel :",prime)
    for courbe in [CourbeElliptique(0,7,prime)]:#generate_random_curves(10,prime):
        ordre = ordre_courbe(courbe)
        print(ordre)
        k = aBonK(courbe,ordre)
        if k:
            point = recup_generateur(courbe)
            print("Le générateur est :",point.x.nb,point.x.nb)
            print("Courbe :",courbe)
            print("Ordre :",ordre)
            print("A K >= 12 : ",k)
            print(point.x,point.y)
