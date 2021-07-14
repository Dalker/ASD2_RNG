"""
Test de l'uniformité de random.uniform

Author: Dalker
Date: 2021-07-08
"""

import random
import matplotlib.pyplot as plt


def spectral(N, axes, rng=None, titre=None):
    """Tirer N nombres au hasard et en étudier le spectre."""
    if titre is not None:
        axes.set_title(titre)

    if rng is None:
        vals = [random.uniform(0, 1) for _ in range(N)]
    else:
        vals = [rng() for _ in range(N)]

    # changer de couleur à chaque colonne pour plus de lisibilité
    for x, y in zip(vals[:N-1], vals[1:]):
        axes.plot(x, y, ".b")

    axes.set_xlabel("n")
    axes.set_ylabel("n+1")


class lcg():
    """Genérateur à congruence linéaire."""
    def __init__(self, m, a, c=0, seed=None):
        """Initialiser le générateur LCG."""
        self.m = m
        self.a = a
        self.c = c
        self.n = seed

    def random(self):
        """Fournir le prochain nombre pseudo-aléatoire."""
        self.n = (self.a * self.n + self.c) % self.m
        return self.n / self.m


SEED = 42
N = 5000
random.seed(SEED)
trng = random.SystemRandom()
lcgibm = lcg(2**31, 65539, seed=SEED)

_, axes = plt.subplots(1, 3)

spectral(N, axes[0], rng=lcgibm.random, titre="LCG(IBM)")
spectral(N, axes[1], titre="Mersenne Twister")
spectral(N, axes[2], rng=trng.random, titre="SystemRandom")
plt.show()
