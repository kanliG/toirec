from MRD import MRDOI


def add_motion_artifacts(ks3d=None):
    motion_im3d = np.zeros(np.shape(ks3d))
    motion_ks3d = np.zeros(np.shape(ks3d), dtype=complex)

    # per slice
    for i in range(0, np.shape(ks3d)[0]):
        ks = ks3d[i, :, :]
        ks_new = ks
        min_rand = 2
        max_rand = np.shape(ks3d)[1] / 50
        step = random.uniform(min_rand, max_rand)
        for ii in range(0, np.shape(ks)[1], int(step)):  # int(step)
            ks_new[:, ii] = ks[:, ii] * (0.2 + 0.2j)

        # Noisy reconstructed image
        noisy_im = MRDOI.recon_corrected_kspace(ks_new)

        motion_im3d[i, :, :] = noisy_im
        motion_ks3d[i, :, :] = ks_new

    return motion_im3d, motion_ks3d


def add_noise_artifacts(ks3d=None):
    noisy_im3d = np.zeros(np.shape(ks3d))
    noisy_ks3d = np.zeros(np.shape(ks3d), dtype=complex)

    # per slice
    mean = 0  # keep it 0
    min_rand = 1
    max_rand = 1.5
    var = 0.5
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


def hanning_filter(ks3d=None):
    hanning_im3d = np.zeros(np.shape(ks3d))
    hanning_ks3d = np.zeros(np.shape(ks3d), dtype=complex)

    # per slice
    mean = 0  # keep it 0
    min_rand = 1
    max_rand = 1.5
    var = 0.5
    sigma = random.uniform(min_rand, max_rand)  # random value for [1 1.5]
    for i in range(0, np.shape(ks3d)[0]):
        ks = ks3d[i, :, :]
        sz = np.shape(ks)
        hanning = ks * window('hann', ks.shape)
        ks_new = hanning

        # Noisy reconstructed image
        hanning_im = MRDOI.recon_corrected_kspace(ks_new)

        hanning_im3d[i, :, :] = hanning_im
        hanning_ks3d[i, :, :] = ks_new

    return hanning_im3d, hanning_ks3d


def add_high_pass_filter_artifacts():
    return


def add_low_pass_filter_artifacts():
    return