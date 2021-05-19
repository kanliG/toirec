# toirec

MRD package is the package that load the raw data, modify the raw data to k-space, reconstruction the k-space, and the effect various modifications before or after the inverse Fourier transform.


I suggest to start with loadMRD_GK.ipynb 


I run it with:
    - Python 3.8.5
Required Packages for Python 3:
    - NumPy: handles FFT transforms and array operations
    - random:use random artifact and noise per call
    - scikit-image: image process (hanning filter)
    - mmapi -array -struct -os -fnmatch -glob -re
        


