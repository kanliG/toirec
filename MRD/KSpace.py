import numpy as np
from MRD import MRDOI
import random
from skimage.filters import window  # hanning filter


# Add motion artifacts in the kspace
#
# Output:
# motion_im3d - 3D kspace with motion
# motion_ks3d - 3D reconstructed image with motion
#
# Input:
# ks3d - 3D kspace
def add_motion_artifacts(ks3d=None):
    ks3d_copy = ks3d.copy()
    motion_im3d = np.zeros(np.shape(ks3d_copy))
    motion_ks3d = np.zeros(np.shape(ks3d_copy), dtype=complex)

    # per slice
    for i in range(0, np.shape(ks3d_copy)[0]):
        ks = ks3d_copy[i, :, :]
        ks_new = ks
        min_rand = 2
        max_rand = np.shape(ks3d_copy)[1]/50
        step = random.uniform(min_rand, max_rand)
        for ii in range(0, np.shape(ks)[1], int(step)):  # int(step)
            ks_new[:, ii] = ks[:, ii] * (0.2 + 0.2j)

        # Noisy reconstructed image
        noisy_im = MRDOI.recon_corrected_kspace(ks_new)

        motion_im3d[i, :, :] = noisy_im
        motion_ks3d[i, :, :] = ks_new

    return motion_im3d, motion_ks3d


# Add noise artifacts in the kspace
#
# Output:
# motion_im3d - 3D kspace with noise
# motion_ks3d - 3D reconstructed image with noise
#
# Input:
# ks3d - 3D kspace
def add_noise_artifacts(ks3d=None):
    noisy_im3d = np.zeros(np.shape(ks3d))
    noisy_ks3d = np.zeros(np.shape(ks3d), dtype=complex)

    # per slice
    mean = 0  # keep it 0
    point = np.abs(ks3d.mean())*40
    min_rand = point/5 # np.abs(ks3d.max())/400
    max_rand = point
    var = max_rand/10
    sigma = random.uniform(min_rand, max_rand)  # random value for [1 1.5]
    for i in range(0, np.shape(ks3d)[0]):
        ks = ks3d[i, :, :]
        sz = np.shape(ks)
        sigma_slice = random.uniform(sigma - var, sigma + var)
        # print(sigma_slice)
        gauss = np.random.normal(mean, sigma_slice, sz)
        gauss = gauss.reshape(sz)
        noise = np.ones(np.shape(ks), dtype=complex) * gauss
        ks_new = ks + noise

        # Noisy reconstructed image
        noisy_im = MRDOI.recon_corrected_kspace(ks_new)

        noisy_im3d[i, :, :] = noisy_im
        noisy_ks3d[i, :, :] = ks_new

    return noisy_im3d, noisy_ks3d


# Implement hanning filter in the kspace
#
# Output:
# motion_im3d - 3D kspace with hanning filter
# motion_ks3d - 3D reconstructed image with hanning filter
#
# Input:
# ks3d - 3D kspace
def hanning_filter(ks3d=None):
    hanning_im3d = np.zeros(np.shape(ks3d))
    hanning_ks3d = np.zeros(np.shape(ks3d), dtype=complex)

    for i in range(0, np.shape(ks3d)[0]):
        ks = ks3d[i, :, :]
        sz = np.shape(ks)
        hanning = ks + ks * window('hann', ks.shape)
        ks_new = hanning

        # Noisy reconstructed image
        hanning_im = MRDOI.recon_corrected_kspace(ks_new)

        hanning_im3d[i, :, :] = hanning_im
        hanning_ks3d[i, :, :] = ks_new

    return hanning_im3d, hanning_ks3d


# Implement high pass filter in the kspace (# We don't need it now)
#
# Output:
# motion_im3d - 3D kspace with high pass filter
# motion_ks3d - 3D reconstructed image with high pass filter
#
# Input:
# ks3d - 3D kspace
def add_high_pass_filter_artifacts():
    return


# Implement low pass filter in the kspace (# We don't need it now)
#
# Output:
# motion_im3d - 3D kspace with low pass filter
# motion_ks3d - 3D reconstructed image with low pass filter
#
# Input:
# ks3d - 3D kspace
def add_low_pass_filter_artifacts(ks3d=None):
    ks3d_copy = ks3d.copy()
    lpass_im3d = np.zeros(np.shape(ks3d_copy))
    lpass_ks3d = np.zeros(np.shape(ks3d_copy), dtype=complex)

    for i in range(0, np.shape(ks3d_copy)[0]):
        ks = ks3d_copy[i, :, :]
        min_rand = np.shape(ks)[0]/10
        max_rand = np.shape(ks)[0]/6
        radius = random.uniform(min_rand, max_rand)  # random value for [1 1.5]

        r = np.hypot(*ks.shape) / 2 * radius / 100
        rows, cols = np.array(ks.shape, dtype=int)
        a, b = np.floor(np.array((rows, cols)) / 2).astype(np.int)
        y, x = np.ogrid[-a:rows - a, -b:cols - b]
        mask = x * x + y * y <= r * r
        ks[~mask] = 0

        # Noisy reconstructed image
        noisy_im = MRDOI.recon_corrected_kspace(ks)

        lpass_im3d[i, :, :] = noisy_im
        lpass_ks3d[i, :, :] = ks

    return lpass_im3d, lpass_ks3d, radius
    
  