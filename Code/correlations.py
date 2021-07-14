"""
Test de predictibilité des valeurs suivantes.

Author: Dalker
Date: 2021-07-08
"""

import rng
import matplotlib.pyplot as plt
import numpy as np

N_ESSAIS = 8000
SEED = 2021


def correlation(x, y):
    """Calcul simple de corrélation linéaire entre deux séries de données."""
    # 1) recentrer les données
    x = np.array(x) - np.mean(x)
    y = np.array(y) - np.mean(y)
    # 2) calculer la corrélation linéaire
    c = x @ y / (np.sqrt(x @ x) * np.sqrt(y @ y))
    # on pourrait aussi tester des corrélations non-linéaires...
    return abs(c)  # ça nous suffit pour ces tests


def test_spectral(generateur, axes, N=N_ESSAIS, title="", seed=None):
    """Tirer N nombres au hasard et en faire l'histogramme."""
    # calcul des valeurs
    vals = [generateur.random() for _ in range(N)]

    # tracé
    axes.set_title(title)
    axes.plot(vals[:N-1], vals[1:], '.b')
    print("* corrélations pour", title, ":")
    print("  lin-lin {:.3f}".format(correlation(vals[:N-1], vals[1:])),
          end=', ')
    print("lin-log {:.3f}".format(correlation(vals[:N-1], np.log(vals[1:]))),
          end=', ')
    print("log-lin {:.3f}".format(correlation(np.log(vals[:N-1]), vals[1:])),
          end=', ')
    print("log-log {:.3f}".format(correlation(np.log(vals[:N-1]),
                                              np.log(vals[1:]))))
    axes.set_xlabel("étape $n$")
    axes.set_ylabel("étape $n+1$")


_, axes = plt.subplots(nrows=2, ncols=3)
test_spectral(rng.VonNeumann(seed=36000000), axes[0, 0],
              title="VonNeumann")
test_spectral(rng.LCG(7, 3, seed=SEED), axes[0, 1], title="LCG a=3 mod 7")
test_spectral(rng.LCG(2**31, 65539, seed=SEED), axes[0, 2],
              title="LCG RANDU(IBM)")
test_spectral(rng.MT(seed=SEED), axes[1, 0], title="Mersenne Twister")
test_spectral(rng.System(), axes[1, 1], title="RNG de l'OS")
test_spectral(rng.SY(0, 1, -1), axes[1, 2], title="Saito-Yamaguchi")
plt.show()
