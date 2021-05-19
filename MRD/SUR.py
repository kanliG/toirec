import bm3d
import numpy as np
from skimage import morphology


# Denoise MRI by bm3d
#
# Output:
# img_new - Denoised MRI
#
# Input:
# img - MRI 2D matrix
# sigma - Std. dev. of the noise
def denoise_bm3d(img=None, sigma=None):
    img_new = img * 0
    img_new = bm3d.bm3d(img, sigma_psd=sigma, stage_arg=bm3d.BM3DStages.ALL_STAGES)
    # stage_arg=bm3d.BM3DStages.HARD_THRESHOLDING)
    return img_new


# calculate SNR - signal to noise ratio
#
# Output:
# snr - signal to noise ratio: double
# bw - binary image of the subject
# mask_noise - binary image of the noise areas
#
# Input:
# image - MRI 2D matrix
# rescale - size of the nose region: int [0 1]
def get_snr(image=None, rescale=0.5):
    # find the image size
    size_x = np.shape(image)[0]
    size_y = np.shape(image)[1]
    # create the object mask
    bw = create_mask(image=image)
    bw[bw > 0] = 1
    # removing small objects
    selem = morphology.disk(2)
    res = morphology.white_tophat(bw, selem)
    bw = bw - res
    # create the boundaries of the object mask
    boundaries = create_boundaries(bw)
    # find the limits of the object
    min_x = min(boundaries[:, 0])
    min_y = min(boundaries[:, 1])
    if min_y < 10:
        min_y = 10
    if min_x < 10:
        min_x = 10

    # Calculate the mean of the signal (only signal, without noise)
    im_signal = np.multiply(image, bw)
    signal = im_signal.flatten()
    signal = signal[signal != 0]
    mean_signal = np.mean(signal)

    # find the noise regions
    # Noise: create four rectangles on the four corners
    size_rect = np.ones(2, dtype=int)
    size_rect = np.multiply([min_x, min_y], rescale)
    size_rect = np.round(size_rect)
    if size_rect[0] < 10:
        size_rect[0] = 10
    if size_rect[1] < 10:
        size_rect[1] = 10
    if size_rect[0] > size_x / 4:
        size_rect[0] = size_x / 4
    if size_rect[1] > size_y / 4:
        size_rect[1] = size_y / 4
    size_rect = size_rect.astype(int)

    mask_noise = np.zeros(shape=[size_x, size_y])
    rect = np.ones(shape=(size_rect[0], size_rect[1]), dtype=int)
    mask_noise[0:size_rect[0], 0:size_rect[1]] = rect
    mask_noise[size_x - size_rect[0]:size_x, 0:size_rect[1]] = rect
    mask_noise[0:size_rect[0], size_y - size_rect[1]:size_y] = rect
    mask_noise[size_x - size_rect[0]:size_x, size_y - size_rect[1]:size_y] = rect

    # maskS = bw
    mask_noise[mask_noise > 0] = 1
    mask_noise[mask_noise <= 0] = 0
    im_noise = np.multiply(image, mask_noise)
    noise = im_noise.flatten()
    noise = noise[noise != 0]
    std_noise = np.std(noise)

    snr = mean_signal / std_noise

    return snr, bw, mask_noise


# Create the boundaries: Find the positions of the binary image
#
# Output:
# bw - binary image
#
# Input:
# boundaries - the boundaries positions
def create_boundaries(bw=None):
    count = 0
    boundarie = np.empty(shape=[bw.shape[0] * bw.shape[1], 2], dtype=int)
    for x in range(0, bw.shape[0]):
        for y in range(0, bw.shape[1]):
            if bw[x, y] == 1:
                boundarie[count, 0] = x
                boundarie[count, 1] = y
                count += 1
    boundaries = boundarie[1:count, :]
    return boundaries


# Create Mask
#
# Output:
# bw - binary image
#
# Input:
# image - image
def create_mask(image=None):
    from skimage.filters import threshold_multiotsu
    # Applying multi-Otsu threshold for the default value, generating three classes.
    thresholds = threshold_multiotsu(image, classes=2)
    # Using the threshold values, we generate the three regions.
    regions = np.digitize(x=image, bins=thresholds)
    bw = np.array(regions)
    return bw
