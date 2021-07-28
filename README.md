# Third_Touch

## Try to static analyse image ,sort them after quality and make some modifications like denoising ,contrast strechting histogram equalization and etc.

### This code rely heavily on project from other people 
## Dependencies:

* Image Magick : sudo apt-get install imagemagick imagemagick-doc 
* [singleLDR2HDR](https://github.com/ray075hl/singleLDR2HDR)
* [entropy-preserving-mapping-prior](https://github.com/bigmms/entropy-preserving-mapping-prior)
* [dctdenoising](https://github.com/gfacciol/DCTdenoising)
* [AGCWD](https://github.com/qyou/AGCWD)

## singleLDR2HDR:(for Intel)
* sudo apt-get install intel-mkl
* python -m pip install git+https://github.com/haasad/PyPardisoProject@0.3.2
> Now go to src and change in wls_filter.py from
* from scipy.sparse.linalg import spsolve, lsqr
> to 
* from scipy.sparse.linalg import lsqr
* from pypardiso import spsolve

It takes huge amouunt of memory. I recommend to limit memory with ulimit becouse if it goes beyond your PC memory if you dont use an SSD you probably will
not live not long enough so see it finish.

