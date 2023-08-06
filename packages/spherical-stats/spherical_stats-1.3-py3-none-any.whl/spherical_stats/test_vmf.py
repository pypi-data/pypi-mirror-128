import numpy as np
import spherical_stats
from time import time

theta = np.array([np.deg2rad(80)])
phi = np.array([0.5])

MU = spherical_stats.polar_to_vectors(theta, phi).T.ravel()

KAPPA = 15

vmf_1 = spherical_stats.VMF(MU, 15)

vmfsamples = vmf_1.rvs(5000)

t0 = time()
vmfsamples = vmf_1.rvs(5000)
print(time() - t0)

vmf_2 = spherical_stats.VMF()

vmf_2.fit(vmfsamples)

t0 = time()
vmf_2.fit(vmfsamples)
print(time() - t0)

print("TRUE: ", MU)
print("FITTED: ", vmf_2.mu)