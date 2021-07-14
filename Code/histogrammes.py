"""
Test de l'uniformité de random.uniform

Author: Dalker
Date: 2021-07-08
"""

import rng
import matplotlib.pyplot as plt
import scipy.stats as stats

N_ESSAIS = 8000
SEED = 2021


def histogramme(generateur, axes, N=N_ESSAIS, title="", seed=None):
    """Tirer N nombres au hasard et en faire l'histogramme."""
    # calcul des valeurs
    vals = [generateur.random() for _ in range(N)]

    # test de chi-carré
    freqs = [0] * 10  # réceptacles pour fréquences
    for val in vals:
        freqs[int(10*val)] += 1
    cs = round(stats.chisquare(freqs).statistic, 2)
    print(title, "a une valeur de chi carré de", cs)

    # tracé
    axes.set_title(title)
    # density=True normalise (aire totale = 1)
    _, _, patches = axes.hist(vals, bins=[0.1*j for j in range(11)],
                              density=True)
    # changer de couleur à chaque colonne pour plus de lisibilité
    for j, patch in enumerate(patches):
        patch.set_facecolor("rg"[j % 2])
    # axes.set_xlabel(f"chi carré = {cs}")


_, axes = plt.subplots(nrows=2, ncols=3)
histogramme(rng.VonNeumann(seed=36000000), axes[0, 0],
            title="VonNeumann")
histogramme(rng.LCG(7, 3, seed=SEED), axes[0, 1], title="LCG a=3 mod 7")
histogramme(rng.LCG(2**31, 65539, seed=SEED), axes[0, 2],
            title="LCG RANDU(IBM)")
histogramme(rng.MT(seed=SEED), axes[1, 0], title="Mersenne Twister")
histogramme(rng.System(), axes[1, 1], title="RNG de l'OS")
histogramme(rng.SY(0, 1, -1), axes[1, 2], title="Saito-Yamaguchi")
plt.show()
