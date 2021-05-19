import MRD
import matplotlib.pyplot as plt
import numpy as np


# Python3 program to search an element
# in row-wise and column-wise sorted matrix
# Searches the element x in mat[][]. If the
# element is found, then prints its position
# and returns true, otherwise prints "not found"
# and returns false
def search(mat, n, x):
    i = 0
    # set indexes for top right element
    j = n - 1
    while i < n and j >= 0:
        if mat[i][j] == x:
            print("n Found at ", i, ", ", j)
            return 1
        if mat[i][j] > x:
            j -= 1
        # if mat[i][j] < x
        else:
            i += 1
    print("Element not found")
    return 0  # if (i == n || j == -1 )


def test_noise(subject=None, scan=None):
    print('**** Start Analysis: %s: SubjectID: %d - ScanID: %d\n', subject, scan)
    [k_space, im] = MRD.MRDOI.recon_mrd_fse2d(mouse_id=subject, scan_id=scan)
    print(np.shape(im))
    plt.figure(1)
    plt.subplot(121)
    plt.imshow(abs(im[5, :, :]), cmap='gray', vmin=0)
    plt.title('im', fontweight="bold")
    plt.subplot(122)
    plt.imshow(abs(k_space[5, :, :]), cmap='gray', vmin=0)
    plt.title('k_space', fontweight="bold")
    # plt.show()

    print('**** Apply hanning \n')
    [hanning_im, hanning_k_space] = MRD.hanning_filter(ks3d=k_space)
    fig = plt.figure(2, figsize=(10, 10))
    plt.subplot(221)
    plt.imshow(abs(im[6, :, :]), cmap='gray', vmin=0)
    plt.title('Original', fontweight="bold")
    plt.axis('off')
    plt.subplot(222)
    plt.imshow(abs(k_space[6, :, :]), cmap='gray', vmin=0)
    plt.title('k_space', fontweight="bold")
    plt.axis('off')
    plt.subplot(223)
    plt.imshow(hanning_im[6, :, :], cmap='gray', vmin=0)
    plt.title('Hanning', fontweight="bold")
    plt.axis('off')
    plt.subplot(224)
    plt.imshow(abs(hanning_k_space[6, :, :]), cmap='gray', vmin=0)
    plt.title('hanning_k_space', fontweight="bold")
    plt.axis('off')
    fig.savefig('apply_Hanning_in_k-space.jpg')  # save results
    # plt.show()

    print('**** Add motion artifact \n')
    [motion_im, k_space_motion] = MRD.add_motion_artifacts(ks3d=k_space)
    plt.figure(3)
    plt.subplot(321)
    plt.imshow(abs(im[5, :, :]), cmap='gray', vmin=0)
    plt.title('im', fontweight="bold")
    plt.subplot(322)
    plt.imshow(abs(k_space[5, :, :]), cmap='gray', vmin=0)
    plt.title('k_space', fontweight="bold")
    plt.subplot(323)
    plt.imshow(hanning_im[5, :, :], cmap='gray', vmin=0)
    plt.title('hanning_im', fontweight="bold")
    plt.subplot(324)
    plt.imshow(abs(k_space_motion[5, :, :]), cmap='gray', vmin=0)
    plt.title('k_space_motion', fontweight="bold")
    plt.subplot(325)
    plt.imshow(motion_im[5, :, :], cmap='gray', vmin=0)
    plt.title('motion_im', fontweight="bold")
    plt.subplot(326)
    plt.imshow(abs(k_space_motion[5, :, :]), cmap='gray', vmin=0)
    plt.title('k_space_motion', fontweight="bold")
    # plt.show()

    print('**** Add noise in K-space \n')
    [noisy_im, k_space_noisy] = MRD.add_noise_artifacts(ks3d=k_space)
    plt.figure(4)
    plt.subplot(221)
    plt.imshow(abs(im[5, :, :]), cmap='gray', vmin=0)
    plt.title('im', fontweight="bold")
    plt.subplot(222)
    plt.imshow(abs(k_space[5, :, :]), cmap='gray', vmin=0)
    plt.title('k_space', fontweight="bold")
    plt.subplot(223)
    plt.imshow(noisy_im[6, :, :], cmap='gray', vmin=0)
    plt.title('noisy_im', fontweight="bold")
    plt.subplot(224)
    plt.imshow(abs(k_space_noisy[5, :, :]), cmap='gray', vmin=0)
    plt.title('k_space_noisy', fontweight="bold")
    plt.show()


# Press the green button in the gutter to run the script.
def test_hanning(subject=None, scan=None):
    print('**** Start Analysis: %s: SubjectID: %d - ScanID: %d\n', subject, scan)
    [k_space, im] = MRD.MRDOI.recon_mrd_fse2d(mouse_id=subject, scan_id=scan)

    print('**** Add noise in K-space \n')
    [hann_im, k_space_hann] = MRD.hanning_filter(ks3d=k_space)
    plt.figure()
    plt.subplot(221)
    plt.imshow(abs(im[5, :, :]), cmap='gray', vmin=0)
    plt.title('im', fontweight="bold")
    plt.subplot(222)
    plt.imshow(abs(k_space[5, :, :]), cmap='gray', vmin=0)
    plt.title('k_space', fontweight="bold")
    plt.subplot(223)
    plt.imshow(hann_im[5, :, :], cmap='gray', vmin=0)
    plt.title('noisy_im', fontweight="bold")
    plt.subplot(224)
    plt.imshow(abs(k_space_hann[5, :, :]), cmap='gray', vmin=0)
    plt.title('k_space_noisy', fontweight="bold")
    plt.show()


def test_snr(subject=None, scan=None):
    print('**** Start Analysis: %s: SubjectID: %d - ScanID: %d\n', subject, scan)
    [k_space, im] = MRD.MRDOI.recon_mrd_fse2d(mouse_id=subject, scan_id=scan)
    im_input = abs(im[5, :, :])
    [snr, bw, mask_noise] = MRD.SUR.get_snr(image=im_input, rescale=0.8)

    print('**** Add noise in K-space \n')
    plt.figure()
    plt.subplot(121)
    plt.title('Original image')
    plt.imshow(im_input, cmap='gray')
    plt.axis('off')
    bw[bw == 1] = 2
    plt.subplot(122)
    plt.title('SNR: ' + str(snr))
    plt.imshow(bw + mask_noise, cmap='gray')
    plt.axis('off')
    plt.show()


def test_low_pass(subject=None, scan=None):
    print('**** Start Analysis: %s: SubjectID: %d - ScanID: %d\n', subject, scan)
    [k_space, im] = MRD.MRDOI.recon_mrd_fse2d(mouse_id=subject, scan_id=scan)
    im_input = abs(im[5, :, :])
    [low_im, low_k_space, radium] = MRD.KSpace.add_low_pass_filter_artifacts(ks3d=k_space)
    print(radium)

    print('**** Add noise in K-space \n')
    ks1 = abs(k_space[5, :, :])
    ks1[ks1 == 0] = 1
    ks1 = np.log(ks1)
    ks2 = abs(low_k_space[5, :, :])
    ks2[ks2 == 0] = 1
    ks2 = np.log(ks2)
    plt.figure()
    plt.subplot(221)
    plt.imshow(abs(im[5, :, :]), cmap='gray', vmin=0)
    plt.title('im', fontweight="bold")
    plt.subplot(222)
    plt.imshow(ks1, cmap='gray', vmin=0)
    plt.title('k_space', fontweight="bold")
    plt.subplot(223)
    plt.imshow(abs(low_im[5, :, :]), cmap='gray', vmin=0)
    plt.title('low_im', fontweight="bold")
    plt.subplot(224)
    plt.imshow(ks2, cmap='gray', vmin=0)
    plt.title('low_k_space', fontweight="bold")
    plt.show()


if __name__ == '__main__':
    # Loop through SubjectID selection
    print('**** Start Extracts: Loop through SubjectID selection')
    # FSE Scans - from all projects
    # my_sheet = "FSE Scans"
    # file_name = 'SQL\\FSEScans.xlsx'  # change it to the name of your excel file
    # ProjectSubjectsScans = pd.read_excel(file_name, sheet_name=my_sheet)
    # ListOfSubjects = ProjectSubjectsScans.Subject_id
    # ListOfScans = ProjectSubjectsScans.Scan_id
    # print(ListOfSubjects[160])
    # print(ListOfScans[160])
    #
    # # Extracts data
    # print('**** Start Modify data')
    # nSubjects = np.shape(ListOfSubjects)[0]
    # for i in [160]:
    subject_id = 2492  # 2  # ListOfSubjects[i]
    scan_id = 29096  # 13323  # ListOfScans[i]

    # test_noise(subject=subject_id, scan=scan_id)
    # test_hanning(subject=subject_id, scan=scan_id)
    # test_snr(subject=subject_id, scan=scan_id)
    test_low_pass(subject=subject_id, scan=scan_id)

    print('**** DONE ')
