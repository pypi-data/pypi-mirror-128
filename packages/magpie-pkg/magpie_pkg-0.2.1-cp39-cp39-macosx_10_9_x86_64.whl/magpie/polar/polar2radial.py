import numpy as np


def get_polar_area2d(redges, pedges):
    """Returns the area of each pixel in the polar coordinate grid.

    Parameters
    ----------

    Returns
    -------
    area2d : ndarray
        The area of each pixel in the polar coordinate grid.
    """
    dp = pedges[1] - pedges[0]
    area = np.pi*(redges[1:]**2. - redges[:-1]**2.)*(dp)/(2.*np.pi)
    area2d = np.array([area for i in range(0, len(pedges)-1)])
    return area2d


def get_pixarea(xedges, yedges):
    """Returns the area of each pixel.

    Parameters
    ----------
    xedges : ndarray
        Edges of the x-coordinate grid.
    yedges : ndarray
        Edges of the y-coordinate grid.

    Returns
    -------
    pixarea : float
        The area of each pixel in the cartesian grid.
    """
    pixarea = (xedges[1]-xedges[0])*(yedges[1]-yedges[0])
    return pixarea


def polar2radial(f, area2d, pixarea, sigma=None, w=None):
    """Calculates the radial mean of data provided in a polar coordinate grid
    which originates from a 2D cartesian grid.

    Parameters
    ----------
    f : ndarray
        2D array of a function f in polar coordinates.
    area2d : ndarray
        The area of each pixel in the polar coordinate grid.
    pixarea : float
        The area of each pixel in the cartesian grid.
    sigma : ndarray
        2D array of the noise for function f in polar coordinates.
    w : ndarray
        2D array containing weights for each pixel in polar grid, ideal for adding
        a binary mask.

    Returns
    -------
    f_radial : array
        Radial profile of f.
    sigma_radial : array
        If sigma is provided then the radial errors are outputted.
    """
    if w is None:
        # without weights, calculate simple mean
        f_radial = np.sum(f, axis=0)/float(len(f))
        if sigma is not None:
            # standard error with corrections for pixel size
            sigma_radial = np.sqrt(np.sum((pixarea/area2d)*sigma**2., axis=0)/(float(len(f))**2.))
    else:
        # with weights, calculate weighted mean
        f_radial = np.sum(f*w, axis=0)/np.sum(w, axis=0)
        if sigma is not None:
            # standard weighted error with corrections for pixel size
            sigma_radial = np.sqrt(np.sum((pixarea/area2d)*(w*sigma)**2., axis=0)/(np.sum(w, axis=0)**2.))
    # returns results
    if sigma is not None:
        return f_radial, sigma_radial
    else:
        return f_radial
