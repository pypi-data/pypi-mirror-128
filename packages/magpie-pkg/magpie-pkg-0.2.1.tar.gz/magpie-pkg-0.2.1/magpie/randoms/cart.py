import numpy as np


def randoms_1d(size, xmin=0., xmax=1.):
    """Returns uniform randoms in 1D.

    Parameters
    ----------
    size : int
        Number of randoms to produce.
    xmin : float, optional
        Minimum value.
    xmax : float, optional
        Maximum value.

    Returns
    -------
    xrands : array
        Uniform randoms in 1D.
    """
    xrands = (xmax - xmin)*np.random.random_sample(size) + xmin
    return xrand


def randoms_2d(size, mins=[0., 0.], maxs=[1., 1.]):
    """Returns uniform randoms in 2D.

    Parameters
    ----------
    size : int
        Number of randoms to produce.
    mins : float, optional
        Minimum values.
    maxs : float, optional
        Maximum values.

    Returns
    -------
    xrands, yrands : array
        Uniform randoms in 2D.
    """
    xrands = randoms_1d(size, xmin=mins[0], xmax=mins[0])
    yrands = randoms_1d(size, xmin=mins[1], xmax=maxs[1])
    return xrands, yrands


def randoms_3d(size, mins=[0., 0., 0], maxs=[1., 1., 1.]):
    """Returns uniform randoms in 3D.

    Parameters
    ----------
    size : int
        Number of randoms to produce.
    mins : float, optional
        Minimum values.
    maxs : float, optional
        Maximum values.

    Returns
    -------
    xrands, yrands, zrands : array
        Uniform randoms in 3D.
    """
    xrands = randoms_1d(size, xmin=mins[0], xmax=mins[0])
    yrands = randoms_1d(size, xmin=mins[1], xmax=maxs[1])
    zrands = randoms_1d(size, xmin=mins[2], xmax=maxs[2])
    return xrands, yrands, zrands
