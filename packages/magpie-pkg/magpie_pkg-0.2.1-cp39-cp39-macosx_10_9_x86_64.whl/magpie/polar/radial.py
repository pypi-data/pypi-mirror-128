import numpy as np


def cumulative_radial(redges, f, sigma=None):
    """Returns the cumulative radial profile and errors if errors are given.

    Parameters
    ----------
    redges : array
        Edges of the radial bins.
    f : array
        Radial profile.
    sigma : array, optional
        Radial errors.

    Returns
    -------
    cumulative_f : array
        Cumulative radial profile.
    cumulative_sigma : array
        If sigma is given then the cumulative errors are computed.
    """
    area = np.pi*(redges[1:]**2. - redges[:-1]**2.)
    f_area = area*f
    cumulative_f = np.zeros(len(redges))
    cumulative_f[1:] = np.cumsum(f_area)
    if sigma is not None:
        cumulative_var = np.zeros(len(redges))
        var_area = (area*sigma)**2.
        cumulative_var[1:] = np.cumsum(var_area)
        cumulative_sigma = np.sqrt(cumulative_var)
    if sigma is None:
        return cumulative_f
    else:
        return cumulative_f, cumulative_sigma
