# Third_Touch

## Try to static analyse image ,sort them after quality and make some modifications like denoising ,contrast strechting histogram equalization and etc.

### This code rely heavily on project from other people 
## Dependencies:

* Image Magick : sudo apt-get install imagemagick imagemagick-doc 
* [singleLDR2HDR](https://github.com/ray075hl/singleLDR2HDR)
* [entropy-preserving-mapping-prior](https://github.com/bigmms/entropy-preserving-mapping-prior)
* [dctdenoising](https://github.com/gfacciol/DCTdenoising)
* [AGCWD](https://github.com/qyou/AGCWD)
* [EnhanceHDR](https://github.com/tuvovan/EnhanceHDR)
* [ICC Color Profile](https://www.color.org/index.xalter)

 
## singleLDR2HDR:(for Intel)
* sudo apt-get install intel-mkl
* python -m pip install git+https://github.com/haasad/PyPardisoProject@0.3.2
> Now go to src and change in wls_filter.py from
* from scipy.sparse.linalg import spsolve, lsqr
> to 
* from scipy.sparse.linalg import lsqr
* from pypardiso import spsolve

It takes huge amount of memory. I recommend to limit memory with ulimit becouse if it goes beyond your PC memory if you dont use an SSD you probably will
not live not long enough so see it finish.

## singleLDR2HDR:(low Memory System)
> ! If the image isnt symmetric this can couse a line in the middle! To reduce the memory usage it split the image into 2 vertical images and after processing put them back together .
* Go to Patch and copy singleLDR2HDR_run.py to the main folder from the singleLDR2HDR project

## FFWT Intel MKL Wrapper
Go to patch -> make -> cp *.so /usr/lib/ -> export LD_PRELOAD="$LD_PRELOAD:/usr/lib/fftw_wrapper.so"
