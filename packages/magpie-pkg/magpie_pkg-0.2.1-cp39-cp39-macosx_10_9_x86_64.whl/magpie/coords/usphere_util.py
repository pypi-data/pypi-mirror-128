import numpy as np


def usphere_area(phi_min, phi_max, theta_min, theta_max):
    """Returns the area for a 'square' segment of a unit sphere given in
    spherical coordinates phi, theta.

    Parameters
    ----------
    phi_min : float
        Minimum latitudinal coordinate in radians (where phi lies [0, 2pi]).
    phi_max : float
        Maximum latitudinal coordinate in radians (where phi lies [0, 2pi]).
    theta_min : float
        Minimum longitudinal coordinate in radians (where theta lies [0, pi]).
    theta_max : float
        Maximum longitudinal coordinate in radians (where theta lies [0, pi]).

    Returns
    -------
    Area : float
        Area in square radians.
    """
    # check phi ranges lie within allowed ranges
    assert phi_min >= 0. and phi_min < 2.*np.pi, "phi_min must lie within [0, 2pi]."
    assert phi_max > 0. and phi_max <= 2.*np.pi, "phi_max must lie within [0, 2pi]."
    assert phi_min != phi_max, "phi_min cannot equal phi_max."
    assert theta_min >= 0. and theta_min < np.pi, "theta_min must lie within [0, pi]."
    assert theta_max > 0. and theta_max <= np.pi, "theta_max must lie within [0, pi]."
    assert theta_min != theta_max, "theta_min cannot equal theta_max."
    # calculate area
    area = (phi_max - phi_min)*(np.cos(theta_min)-np.cos(theta_max))
    return area


def sphere2lonlat(theta):
    """Converts the spherical coordinates theta to the longitude and latitude
    convention (where theta lies [-pi/2., pi/2.].

    Parameters
    ----------
    theta : array
        Latitude given in the range [0., pi] where theta = 0 at the north pole.

    Returns
    -------
    Latitude : array
        Latitude given in the range [-pi/2, pi/2].
    """
    latitude = np.pi/2. - theta
    return latitude



def lonlat2sphere(theta):
    """Converts from latitude to spherical coordinate convention.

    Parameters
    ----------
    Latitude : array
        Latitude given in the range [-pi/2, pi/2].

    Returns
    -------
    theta : array
        Latitude given in the range [0., pi] where theta = 0 at the north pole.
    """
    theta = np.pi/2. - theta
    return theta
