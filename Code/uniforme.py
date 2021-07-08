"""
Test de l'uniformité de random.uniform

Author: Dalker
Date: 2021-07-08
"""

import random
import matplotlib.pyplot as plt


def uniformiser(N, axes, seed=None):
    """Tirer N nombres au hasard et en faire l'histogramme."""
    random.seed(2021)
    vals = [random.uniform(0, 1) for _ in range(N)]

    _, _, patches = axes.hist(vals, bins=[0.1*j for j in range(11)],
                              density=True)
    # density=True normalise (aire totale = 1)

    # changer de couleur à chaque colonne pour plus de lisibilité
    for j, patch in enumerate(patches):
        patch.set_facecolor("rg"[j % 2])

    axes.set_title(f"N={N}")


_, axes = plt.subplots(nrows=2, ncols=2)
uniformiser(100, axes[0, 0])
uniformiser(1000, axes[0, 1])
uniformiser(10000, axes[1, 0])
uniformiser(100000, axes[1, 1])
plt.show()
