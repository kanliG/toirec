# Import the required modules
from scipy import complex_
from MRD import PPR_keywords
import mmap
import numpy as np
import array
import struct
import os
import fnmatch
import glob

# Global
# Windows directory
rootPathMRD = 'O:\\Projects & users applications\\Denoise\\Dataset\\MRDtest\\'
rootPathSUR = 'O:\\Projects & users applications\\Denoise\\Dataset\\MRD\\'

# Linux directory
# rootPathMRD = '/home/ivip/MRI/MRDData/'
# rootPathSUR = '/home/ivip/MRI/OriginalData/'


def get_data_format(dt=None):
    if dt == 0:
        return 'B'
        # datasize = 1
    elif dt == 1:
        return 'b'
        # datasize = 1
    elif dt == 2:
        return 'h'
        # datasize = 2
    elif dt == 3:
        return 'h'
        # datasize = 2
    elif dt == 4:
        return 'l'
        # datasize = 4
    elif dt == 5:
        return 'f'
        # datasize = 4
    elif dt == 6:
        return 'd'
        # datasize = 8
    else:
        # datasize = 4
        return 'i'


def get_mrd_3d(filename_=None):
    # Open file as read-binary only
    fidf = open(filename_, 'r+b')  # open(filename_,'rb')
    fid = mmap.mmap(fidf.fileno(), 0)

    # Read first 4 values from header
    # val = struct.unpack('iiii', fid.read(16))  # Linux
    val = struct.unpack('llll', fid.read(16)) # Windows

    # Get dimensions from this
    no_samples, no_views, no_views_2, no_slices = val[0], val[1], val[2], val[3]

    # Work out datatype of data
    fid.seek(18)
    datatype_ = struct.unpack('h', fid.read(2))[0]
    fid.seek(48)
    # scaling = struct.unpack('f', fid.read(4))
    # bitsperpixel = struct.unpack('f', fid.read(4))

    fid.seek(152)
    val = struct.unpack('ii', fid.read(8))
    no_echoes = val[0]
    no_expts = val[1]

    fid.seek(256)
    # text = fid.read(256)

    dim = [no_expts, no_echoes, no_slices, no_views_2, no_views, no_samples]

    dt = datatype_

    if dt >= 0x10:
        iscomplex = 2
        dt = dt - 0x10
    else:
        iscomplex = 1

    dataformat = get_data_format(dt)

    # Compute the number of values expected to be read from the dimensions
    num2read = no_expts * no_echoes * no_slices * no_views * no_views_2 * no_samples * iscomplex

    fid.seek(512)

    m_total = array.array(dataformat)
    m_total.fromfile(fid, num2read)
    if len(m_total) != num2read:
        print("We have a problem...(file length/read mismatch)")
        return 0

    par = PPR_keywords.ParseKeywords(fid)
    fid.close()

    if iscomplex == 2:
        m_real = m_total[::2]
        m_imag = m_total[1::2]
        m_c = np.vectorize(complex)(m_real, m_imag)
        # m_real = None
        # m_imag = None
        # m_total = None
    else:
        m_c = m_total
        # m_total = None

    n = 0

    ord_ = list(range(no_views))

    if 'VAR_centric_on' in par:
        if int(par['VAR centric_on']) == 1:
            val = int(no_views * 0.5)
            ord_ = list(range(no_views))
            for x in range(val):
                ord_[2 * x] = val + x
                ord_[2 * x + 1] = val - x - 1
    elif 'VAR pe1_order' in par:
        if int(par['VAR pe1_order']) == 1:
            val = int(no_views * 0.5)
            ord_ = list(range(no_views))
            for x in range(val):
                ord_[2 * x] = val + x
                ord_[2 * x + 1] = val - x - 1

    ord2 = list(range(no_views_2))

    if 'pe2_centric_on,' in par:

        if int(par['pe2_centric_on,']) == 1:
            val = int(no_views_2 * 0.5)
            ord2 = list(range(no_views_2))
            for x in range(val):
                ord2[2 * x] = val + x
                ord2[2 * x + 1] = val - x - 1

    im = np.zeros(shape=(no_expts, no_echoes, no_slices, no_views, no_views_2,
                         no_samples), dtype=complex_)

    for a in range(no_expts):
        for b in range(no_echoes):
            for c in range(no_slices):
                for d in range(no_views):
                    for e in range(no_views_2):
                        for f in range(no_samples):
                            im[a][b][c][ord_[d]][ord2[e]][f] = m_c[f + n]
                        n += no_samples

    # ord_ = None
    im = np.squeeze(im)

    return im, dim, par


# Open MRD files!
# Select the MRD files
# Output:
# DATA - kspace
# folderName - The folder name where the data are be stored.
#
# Input:
# titleOFDialog - The title of the dialog box
# mouseID - The mouse ID
# scanID - The scan ID
# Example #1:
# OpenMRDfile(); % Select the MRD file
#
# Example #2:
# OpenMRDfile(titleOFDialog, mouseID, scanID);
# OpenMRDfile('titleOFDialog',1701,20626);
def open_mrd_file(mouse_id=None, scan_id=None):
    full_file_name = create_mrd_path(mouse_id, scan_id)
    [im, dim, par] = get_mrd_3d(full_file_name)
    return im, dim, par


def open_sur_file(mouse_id=None, scan_id=None):
    # im = []
    full_file_name = create_sur_path(mouse_id, scan_id)
    [im1, dim, par] = get_mrd_3d(full_file_name[0])
    im = np.zeros([np.shape(full_file_name)[0], np.shape(im1)[0], np.shape(im1)[1]])
    for i in range(0, np.shape(full_file_name)[0]):
        [im1, _] = get_mrd_3d(full_file_name[i])
        im1 = np.abs(im1)
        im[i, :, :] = im1
    return im, dim, par


def create_mrd_path(mouse_id=None, scan_id=None):
    full_file = str(rootPathMRD + str(int(mouse_id)) + '\\' + str(int(scan_id)) + '\\' + str(int(scan_id)))
    print(full_file)
    full_file_name = full_file + '_0.MRD'
    if not os.path.exists(full_file_name):
        full_file_name = full_file + '_000_0.MRD'
    return full_file_name


def create_rtv_path(mouse_id=None, scan_id=None):
    full_file = str(rootPathMRD + str(int(mouse_id)) + '\\' + str(int(scan_id)) + '\\' + 'rtable.rtv')
    return full_file


def find(pattern, path_input):
    result = []
    for root, dirs, files in os.walk(path_input):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


def create_sur_path(mouse_id=None, scan_id=None):
    full_folder = str(rootPathSUR + str(int(mouse_id)) + '\\Image\\' + str(int(scan_id)) + '\\1\\*.SUR')
    mylist = []
    for file in glob.glob(full_folder):
        mylist.append(file)
    return mylist


def recon_mrd_fse2d(mouse_id=None, scan_id=None):
    im1 = []
    full_file_name_mrd = create_mrd_path(mouse_id, scan_id)
    full_file_name_rtv = create_rtv_path(mouse_id, scan_id)

    if os.path.exists(full_file_name_mrd):
        # open MRD file
        [data, dim, par] = get_mrd_3d(full_file_name_mrd)
        # import pprint
        # pprint.pprint(par)

        # extract the parameters
        if 'NO_SAMPLES' in par:
            no_samples = str(par['NO_SAMPLES'])
            no_samples = [int(s) for s in no_samples.split() if s.isdigit()][0]
        else:
            no_samples = dim[5]
        if 'NO_VIEWS' in par:
            no_views = str(par['NO_VIEWS'])
            no_views = [int(s) for s in no_views.split() if s.isdigit()][0]
        else:
            no_views = dim[4]
        if 'nav_on' in par:
            nav_on = str(par['nav_on'])
            nav_on = [int(s) for s in nav_on.split() if s.isdigit()][0]
        else:
            nav_on = 0
        if 'VIEWS_PER_SEGMENT' in par:
            views_per_seg = str(par['VIEWS_PER_SEGMENT'])
            views_per_seg = [int(s) for s in views_per_seg.split() if s.isdigit()][0]
        else:
            views_per_seg = no_views
        if 'PHASE_ORIENTATION' in par:
            phase_orientation = str(par['PHASE_ORIENTATION'])
            phase_orientation = [int(s) for s in phase_orientation.split() if s.isdigit()][0]
        else:
            phase_orientation = 1
        no_segments = no_views / views_per_seg
        if no_segments > 1:
            reorder1 = 1
        else:
            reorder1 = 0
        no_slices = str(par['NO_SLICES'])
        no_slices = [int(s) for s in no_slices.split() if s.isdigit()][0]
        ks = np.zeros([no_slices, no_samples, no_samples], dtype=complex)
        im = np.zeros([no_slices, no_samples, no_samples], dtype=complex)
        # per slice
        for current_slice in range(0, no_slices):
            if dim[2] > 1:  # if more than one slice
                data_1 = np.squeeze(data[current_slice, :, :])
            else:
                data_1 = np.squeeze(data)

            # Ifft the MRD file
            data_1 = np.fft.ifft(np.fft.ifftshift(data_1, axes=1), axis=1)

            # extract navigators
            if nav_on:
                navigator = np.zeros([views_per_seg, no_samples], dtype=complex)
                for v in range(0, views_per_seg):
                    navigator[v, :] = data_1[v, :]

                data_1 = data_1[views_per_seg:np.shape(data_1)[0], :]

                # phase correction
                nav = 1
                if nav:
                    ph = np.angle(data_1)
                    ph_nav = np.angle(navigator)
                    ph_nav_large = np.tile(ph_nav, (int((no_views - views_per_seg) / views_per_seg), 1))
                    ph_temp = ph - ph_nav_large
                    # mag correction
                    magn0 = np.abs(data_1)

                    im1 = magn0 * np.exp(complex(0, 1) * ph_temp)
                    data_1 = im1

            # phase reorder
            if reorder1:
                if not os.path.exists(full_file_name_rtv):
                    rtable = create_rtable(par)
                else:
                    rtable = np.genfromtxt(full_file_name_rtv)
                rtable[0:views_per_seg] = np.zeros(views_per_seg)
                rtable = rtable[int(views_per_seg):np.shape(rtable)[0]]
                #  rtable = rtable.reshape(int(views_per_seg), int(no_segments - 1), order='F').copy()
                data_2 = data_1 * 0
                for i in range(0, int(no_views - views_per_seg - 1)):
                    data_2[int(rtable[i]), :] = data_1[i, :]
                data_1 = data_2

            # zero-padding
            data_2 = np.zeros([no_samples, no_samples], dtype=complex)
            data_2[0:np.shape(data_1)[0], 0:np.shape(data_1)[1]] = data_1
            data_1 = data_2

            # PE direction: rotation
            if phase_orientation == 1:
                data_1 = np.rot90(data_1, k=-1)
                # store k - space
                corrected_kspace = np.fft.fftshift(np.fft.fft(data_1, axis=0), axes=0)
                ks[current_slice, :, :] = corrected_kspace

                # reconstruction
                fft_on = 1
                if fft_on:
                    im1 = recon_corrected_kspace(corrected_kspace)

            else:
                data_1 = np.flip(data_1, 2)
                # store k - space
                corrected_kspace = np.fft.fftshift(np.fft.fft(data_1, axis=1), axes=1)
                ks[:, :, current_slice] = corrected_kspace

                # reconstruction
                fft_on = 1
                if fft_on:
                    im1 = recon_corrected_kspace(corrected_kspace)

            im[current_slice, :, :] = np.abs(im1)
    else:
        print('**************** error: this path is not exist - PATH: ', full_file_name_mrd)
        ks = []
        im = []

    return ks, im


def recon_corrected_kspace(corrected_kspace=None):
    im = np.fft.ifft(corrected_kspace, axis=1)
    im = np.fft.ifft(im, axis=0)
    im = np.fft.ifftshift(im)
    im = np.abs(im)
    return im


def create_rtable(par=None):
    print('In progress...')
    rtable = par
    return rtable


if __name__ == '__main__':
    pass
