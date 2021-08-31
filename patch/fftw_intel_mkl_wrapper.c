/*******************************************************************************
* Copyright 2005-2019 Intel Corporation.
*
* This software and the related documents are Intel copyrighted  materials,  and
* your use of  them is  governed by the  express license  under which  they were
* provided to you (License).  Unless the License provides otherwise, you may not
* use, modify, copy, publish, distribute,  disclose or transmit this software or
* the related documents without Intel's prior written permission.
*
* This software and the related documents  are provided as  is,  with no express
* or implied  warranties,  other  than those  that are  expressly stated  in the
* License.
*******************************************************************************/

/*
 *
 * fftw_destroy_plan - FFTW3 wrapper to Intel(R) MKL.
 *
 ******************************************************************************
 */

#include <fftw3_mkl.h>

void
fftw_destroy_plan(fftw_plan plan)
{
    if (plan && ((fftw_mkl_plan)plan)->destroy) {
        ((fftw_mkl_plan)plan)->destroy((fftw_mkl_plan)plan);
    }
}
/*******************************************************************************
* Copyright 2005-2019 Intel Corporation.
*
* This software and the related documents are Intel copyrighted  materials,  and
* your use of  them is  governed by the  express license  under which  they were
* provided to you (License).  Unless the License provides otherwise, you may not
* use, modify, copy, publish, distribute,  disclose or transmit this software or
* the related documents without Intel's prior written permission.
*
* This software and the related documents  are provided as  is,  with no express
* or implied  warranties,  other  than those  that are  expressly stated  in the
* License.
*******************************************************************************/

/*
 *
 * fftw_execute - FFTW3 wrapper to Intel(R) MKL.
 *
 ******************************************************************************
 */

//#include <fftw3_mkl.h>

void
fftw_execute(const fftw_plan plan)
{
    fftw_mkl_plan mkl_plan = (fftw_mkl_plan)plan;

    if (!(mkl_plan && mkl_plan->execute)) return;

    mkl_plan->execute(mkl_plan);
}
/*******************************************************************************
* Copyright 2005-2019 Intel Corporation.
*
* This software and the related documents are Intel copyrighted  materials,  and
* your use of  them is  governed by the  express license  under which  they were
* provided to you (License).  Unless the License provides otherwise, you may not
* use, modify, copy, publish, distribute,  disclose or transmit this software or
* the related documents without Intel's prior written permission.
*
* This software and the related documents  are provided as  is,  with no express
* or implied  warranties,  other  than those  that are  expressly stated  in the
* License.
*******************************************************************************/

/*
 *
 * fftw_init_threads - FFTW3 wrapper to Intel(R) MKL.
 *
 ******************************************************************************
 */

//#include <fftw3_mkl.h>

/** Initialize threads. \return 0 on error. */
int
fftw_init_threads(void)
{
    fftw3_mkl.nthreads = MKL_Domain_Get_Max_Threads(MKL_DOMAIN_FFT);
    return 1;
}
/*******************************************************************************
* Copyright 2005-2019 Intel Corporation.
*
* This software and the related documents are Intel copyrighted  materials,  and
* your use of  them is  governed by the  express license  under which  they were
* provided to you (License).  Unless the License provides otherwise, you may not
* use, modify, copy, publish, distribute,  disclose or transmit this software or
* the related documents without Intel's prior written permission.
*
* This software and the related documents  are provided as  is,  with no express
* or implied  warranties,  other  than those  that are  expressly stated  in the
* License.
*******************************************************************************/

/*
 *
 * fftw_plan_dft_r2c_2d - FFTW3 wrapper to Intel(R) MKL.
 *
 ******************************************************************************
 */

//#include <fftw3_mkl.h>

fftw_plan
fftw_plan_dft_r2c_2d(int nx, int ny, double *in, fftw_complex *out,
                     unsigned flags)
{
    int n[2] = { nx, ny };
    return fftw_plan_dft_r2c(2, n, in, out, flags);
}
/*******************************************************************************
* Copyright 2005-2019 Intel Corporation.
*
* This software and the related documents are Intel copyrighted  materials,  and
* your use of  them is  governed by the  express license  under which  they were
* provided to you (License).  Unless the License provides otherwise, you may not
* use, modify, copy, publish, distribute,  disclose or transmit this software or
* the related documents without Intel's prior written permission.
*
* This software and the related documents  are provided as  is,  with no express
* or implied  warranties,  other  than those  that are  expressly stated  in the
* License.
*******************************************************************************/

/*
 *
 * fftw_plan_many_r2r - FFTW3 wrapper to Intel(R) MKL.
 *
 ******************************************************************************
 */

//#include <fftw3_mkl.h>

fftw_plan
fftw_plan_many_r2r(int rank, const int *n, int howmany, double *in,
                   const int *inembed, int istride, int idist, double *out,
                   const int *onembed, int ostride, int odist,
                   const fftw_r2r_kind * kind, unsigned flags)
{
    fftw_iodim64 dims64[MKL_MAXRANK];
    fftw_iodim64 howmany64;
    int i;

    if (rank > MKL_MAXRANK)
        return NULL;

    if (n == NULL)
        return NULL;

    for (i = 0; i < rank; ++i)
    {
        dims64[i].n = n[i];
    }
    if (rank > 0)
    {
        dims64[rank - 1].is = istride;
        dims64[rank - 1].os = ostride;
    }
    if (!inembed)
        inembed = n;
    if (!onembed)
        onembed = n;
    for (i = rank - 1; i > 0; --i)
    {
        dims64[i - 1].is = dims64[i].is * inembed[i];
        dims64[i - 1].os = dims64[i].os * onembed[i];
    }

    howmany64.n = howmany;
    howmany64.is = idist;
    howmany64.os = odist;

    return fftw_plan_guru64_r2r(rank, dims64, 1, &howmany64, in, out, kind,
                                flags);
}
/*******************************************************************************
* Copyright 2005-2019 Intel Corporation.
*
* This software and the related documents are Intel copyrighted  materials,  and
* your use of  them is  governed by the  express license  under which  they were
* provided to you (License).  Unless the License provides otherwise, you may not
* use, modify, copy, publish, distribute,  disclose or transmit this software or
* the related documents without Intel's prior written permission.
*
* This software and the related documents  are provided as  is,  with no express
* or implied  warranties,  other  than those  that are  expressly stated  in the
* License.
*******************************************************************************/

/*
 *
 * fftw_plan_with_nthreads - FFTW3 wrapper to Intel(R) MKL.
 *
 ******************************************************************************
 */

//#include <fftw3_mkl.h>

void
fftw_plan_with_nthreads(int nthreads)
{
    fftw3_mkl.nthreads = nthreads;
}
