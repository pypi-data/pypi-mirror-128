import numpy as np
from scipy import interpolate


def pdf2cdf(xmid, pdf, return_normpdf=True):
    """Calculates the CDF from a given PDF.

    Parameters
    ----------
    xmid : array
        Linearly spaced x-values given at the middle of a bin of length dx.
    pdf : array
        Probabilty distribution function.
    return_normpdf : bool, optional
        Normalise PDF is also outputed.

    Returns
    -------
    x : array
        X-coordinates.
    cdf : array
        Cumulative distribution function with extreme points set 0 and 1.
    normpdf : array, optional
        Normalised PDF.
    """
    dx = xmid[1] - xmid[0]
    x = np.linspace(xmid[0] - 0.5*dx, xmid[-1]+0.5*dx, len(xmid)+1)
    cdf = np.zeros(len(x))
    cdf[1:] = np.cumsum(pdf)*dx
    normpdf = pdf/np.max(cdf)
    cdf /= np.max(cdf)
    if return_normpdf is True:
        return x, cdf, normpdf
    else:
        return x, cdf


def randoms_cdf(x, cdf, size, kind='cubic'):
    """Generates randoms from a given cumulative distribution function.

    Parameters
    ----------
    x : array
        X-coordinates.
    cdf : array
        Cumulative distribution function, extreme points must be 0 and 1 i.e.
        cdf[0] = 0 and cdf[-1] = 1.
    size : int
        Size of the random sample.
    kind : str, optional
        Scipy CDF interpolation kind.

    Returns
    -------
    rands : array
        Randoms drawn from sample CDF.
    """
    assert cdf[0] == 0. and cdf[-1] == 1., "CDF must be defined in the range [0, 1]."
    u_r = np.random.random_sample(size)
    interp_cdf = interpolate.interp1d(cdf, x, kind=kind)
    rands = interp_cdf(u_r)
    return rands


def randoms_pdf(xmid, pdf, size, kind='cubic'):
    """Generates randoms from a given probability distribution function by first
    calculating a CDF.

    Parameters
    ----------
    xmid : array
        Linearly spaced x-values given at the middle of a bin of length dx.
    pdf : array
        Probabilty distribution function.
    size : int
        Size of the random sample.
    kind : str, optional
        Scipy CDF interpolation kind.

    Returns
    -------
    rands : array
        Randoms drawn from sample PDF.
    """
    x, cdf = pdf2cdf(xmid, pdf, return_normpdf=False)
    rands = randoms_cdf(x, cdf, size, kind=kind)
    return rands
