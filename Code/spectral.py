"""
Test de l'uniformité de random.uniform

Author: Dalker
Date: 2021-07-08
"""

import random
import matplotlib.pyplot as plt


def spectral(N, axes, seed=None):
    """Tirer N nombres au hasard et en étudier le spectre."""
    vals = [random.uniform(0, 1) for _ in range(N)]

    # changer de couleur à chaque colonne pour plus de lisibilité
    for x, y in zip(vals[:N-1], vals[1:]):
        axes.plot(x, y, ".b")

    axes.set_xlabel("n")
    axes.set_ylabel("n+1")


_, axes = plt.subplots()
spectral(10000, axes, seed=42)
plt.show()
