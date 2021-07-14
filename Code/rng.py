"""
Implémentations "maison" de quelques PRNG pour le projet dans GymInf/ASD2.

Author: Dalker
Date: 2021-07-08
"""

import random


class RNG:
    """
    Classe abstraite pour définir l'interface commune aux classes qui suivent.

    Attribut commun:
       - seed: la graine (éventuelle) du RNG
       - n: valeur actuelle du nombre pseudo-aléatoire

    Constante commune:
       - LONGUEUR: longueur en bits des nombres à générer (pour les RNG qui
                   en ont besoin explicitement)
    """

    LONGUEUR = 32  # longueur en bits des nombres à générer

    def __init__(self, seed=None):
        """Initialiser le RNG, avec une éventuelle graine."""
        self.seed = seed if seed is not None else 42
        self.n = self.seed

    def random(self):
        """Fournir le prochain nombre pseudo-aléatoire, normalisé à [0, 1]."""
        raise NotImplementedError


class VonNeumann(RNG):
    """RNG basé sur chiffres intermédiaires d'un carré."""

    def __init__(self, seed=None):
        """Initialiser le rng."""
        super().__init__(seed)
        self.n = self.seed

    def random(self):
        """Fournir le prochain nombre."""
        carre = self.n ** 2
        # on enlève le "0b" du début et on ajoute des 0 à gauche si nécessaire
        bits = "{:0>64s}".format(bin(carre)[2:])
        bits = bits[16:48]
        self.n = int(bits, 2)
        return self.n / 2**32


class LCG(RNG):
    """
    Genérateur à congruence linéaire u_{n+1} <- (a*u_n + c) mod m.

    Attributs spécifiques:
    - m: modulo
    - a: facteur multiplicatif
    - c: terme additif
    """

    def __init__(self, m, a, c=0, seed=None):
        """Initialiser le générateur LCG."""
        super().__init__(seed)
        self.m = m
        self.a = a
        self.c = c
        self.n = self.seed

    def random(self):
        """Fournir le prochain nombre pseudo-aléatoire."""
        self.n = (self.a * self.n + self.c) % self.m
        return self.n / self.m


class SY(RNG):
    """
    Générateur de suite chaotique de Saito-Yamaguchi.

    Des bits sont générés successivement comme arrondis d'une racine de
    polynômes successifs de degré 3, garanties dans [0, 1].

    Un polynôme est donné par x^3 + b x^2 + c x + d, et sa racine sera arrondie
    à 1 ssi 1 + 2b + 4c + d < 0. L'évolution au bit suivant se fait via des
    équations algébriques (cf. méthode dédiée).

    Attributs:
    - b, c, d: valeurs actuelles des coefs du polynôme de degré 3 sous-jacent.
    """

    def __init__(self, b, c, d, seed=None):
        """Initialiser à partir des coefs du polynôme initial."""
        super().__init__(seed)
        self.b = b
        self.c = c
        self.d = d

    def _evoluer(self):
        """Passer d'un polynôme au suivant et retourner le bit actuel."""
        eps = 1 if 1 + 2*self.b + 4*self.c + 8*self.d < 0 else 0
        b = 2*self.b + 3*eps
        c = 4*self.c + (4*self.b + 3)*eps
        d = 8*self.d + (4*self.c + 2*self.b + 1)*eps
        self.b, self.c, self.d = b, c, d
        return eps

    def random(self):
        """Fournir le prochain nombre entre 0 et 1 à 32 bits."""
        n = 0
        for _ in range(self.LONGUEUR):
            n *= 2
            n += self._evoluer()

        return n / 2**self.LONGUEUR


class MT(RNG):
    """Mersenne Twister hérité de random."""
    def __init__(self, seed=None):
        """Initialiser la graine."""
        super().__init__(seed)
        random.seed(self.seed)

    def random(self):
        """Fournir prochain nombre entre 0 et 1."""
        return random.uniform(0, 1)


class System(RNG):
    """RNG hérité de l'OS."""
    def __init__(self, seed=None):
        """Initialiser la graine."""
        super().__init__(seed)
        random.seed(self.seed)
        self.sysrand = random.SystemRandom()

    def random(self):
        """Fournir prochain nombre entre 0 et 1."""
        return self.sysrand.uniform(0, 1)


def test(rng):
    """Tester un rng."""
    for _ in range(4):
        print(rng.random())


if __name__ == "__main__":
    # quelques tests
    rng = VonNeumann(seed=36000000)
    print("* VonNeumann avec seed de 2**16 *")
    test(rng)

    rng = LCG(7, 3, seed=1)
    print("* LCG avec modulo 7, a=3 et seed de 1 *")
    test(rng)

    rng = SY(0, 1, -1)
    print("* Saito-Yamaguchi avec b=0, c=1, d=-1 *")
    test(rng)

    rng = MT()
    print("* Mersenne Twister du module random avec seed de 42 *")
    test(rng)

    rng = System()
    print("* RNG de l'OS avec seed (inutilisé) de 42 *")
    test(rng)
