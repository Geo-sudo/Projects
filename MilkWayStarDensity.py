import numpy as np
import matplotlib.pyplot as plt


Psi = 1e-4
RA = 20
RB = 12e3
RC = 5e4
OmegaA = 21
OmegaB = -3
OmegaC = -8


r = np.logspace(0, 5.1, num=500)


def density(r):
    return Psi * (np.exp(OmegaA - r/RA) + np.exp(OmegaB - r/RB) + np.exp(OmegaC - r/RC))

rho_r = density(r)


plt.figure(figsize=(10, 6))
plt.loglog(r, rho_r)
plt.xlabel('Distance from the center of the Milky Way r (light-years)')
plt.ylabel('Density ρ(r) (stars/(light-year)^3)')
plt.title('Numpy and Matplot were used to make the graph. Code is at https://github.com/Geo-sudo/Astrophysics/')
plt.grid(True, which="both", ls="--")
plt.show()

