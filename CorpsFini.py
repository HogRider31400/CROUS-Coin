# -*- coding: utf-8 -*-

class CorpsFini:
    ##Attributs : nb et nb_premier

    def __init__(self, nb, nb_premier):
        if nb >= nb_premier or nb<0:
            error = str(nb)+" n'est pas dans le corps (entre 0 et "+str(nb_premier -1)
            raise ValueError(error)
        self.nb = nb
        self.nb_premier = nb_premier

    def __repr__(self):
        return str(self.nb_premier, self.nb)

    def __eq__(self, other):
        if other is None:
            return False
        return self.nb == other.nb and self.nb_premier == other.nb_premier

    def primeValid(self, other):
        if self.nb_premier != other.nb_premier:
            raise TypeError('On ne peut pas additionner 2 nombres de corps différents')

    def __add__(self, other):
        primeValid(self, other)
        nb = (self.nb + other.nb) % self.nb_premier
        return self.__class__(nb, self.nb_premier)

    def __sub__(self, other):
        primeValid(self, other)
        nb = (self.nb - other.nb) % self.nb_premier
        return self.__class__(nb, self.nb_premier)

    def __mul__(self, other):
        primeValid(self, other)
        nb = (self.nb * other.nb) % self.nb_premier
        return self.__class__(nb, self.nb_premier)

    def __pow__(self, exposant):
        nb = (self.nb **exposant) % self.nb_premier
        return self.__class__(nb, self.nb_premier)

    def __truediv__(self, other):
        '''Fait la division flottante entre a et b : a/b, de toute manière
        le résultat sera entier'''
        primeValid(self, other)
        if (other.nb == 0):
            raise ZeroDivisionError("le diviseur doit être non nul")
        ##Calcul de l'inverse : b^(-1) = b^(nb_premier-2)
        inverse_op2 = other.nb ** ((other.nb_premier)-2)
        return self * self.__class__(inverse_op2, self.nb_premier)

    def __pow__(self, exposant):
        puiss = exposant % (self.nb_premier - 1)
        nb = pow(self.nb, puiss, self.nb_premier)
        return self.__class__(nb, self.nb_premier)