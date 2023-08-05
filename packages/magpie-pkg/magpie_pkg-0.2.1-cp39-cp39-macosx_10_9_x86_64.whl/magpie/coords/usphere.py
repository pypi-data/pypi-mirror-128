import numpy as np

from .. import coords


def usphere_rotate(phi, theta, phi_end, theta_end, phi_start=0., theta_start=0.):
    """Rotate positions on the sky (phi_start, theta_start) to (phi_end, theta_end) along the line of shortest length.


    Parameters
    ----------
    phi : array
        Longitudinal coordinates to be rotated.
    theta : array
        Latitudinal coordinates to be rotated.
    phi_end : float
        End phi rotation point.
    theta_end : float
        End theta rotation point.
    phi_start : float, optional
        Start phi rotation point.
    theta_start : float, optional
        Start theta rotation point.

    Notes
    -----
    Following method outlined on https://math.stackexchange.com/questions/114107/determine-the-rotation-necessary-to-transform-one-point-on-a-sphere-to-another
    by G Cab.
    """
    # sanity checks and ranges
    assert phi_start != phi_end or theta_start != theta_end, "Rotation points must be different."
    assert phi_start >= 0. and phi_start <= 2.*np.pi, "phi_start must lie within [0, 2pi]."
    assert phi_end >= 0. and phi_end <= 2.*np.pi, "phi_end must lie within [0, 2pi]."
    assert theta_start >= 0. and theta_start <= np.pi, "theta_start must lie within [0, pi]."
    assert theta_end >= 0. and theta_end <= np.pi, "theta_end must lie within [0, pi]."
    # determine vector of starting point
    r_start = 1.
    # convert points on the sphere to cartesian coordinates
    x_start, y_start, z_start = coords.sphere2cart(r_start, phi_start, theta_start)
    u = np.array([x_start, y_start, z_start])
    # determine vector of end point but first convert to cartesian coordinates
    x_end, y_end, z_end = coords.sphere2cart(r_start, phi_end, theta_end)
    v = np.array([x_end, y_end, z_end])
    # calculate other dummy variables (n, t, alpha, Rn, T, invT) to do the rotation,
    # see notes to see how these are determined.
    n = np.cross(u, v)
    n /= np.sqrt(np.sum(n**2.))
    t = np.cross(n, u)
    alpha = np.arctan2(v.dot(t), v.dot(u))
    Rn = np.array([[np.cos(alpha), -np.sin(alpha), 0.],
                  [np.sin(alpha),   np.cos(alpha), 0.],
                  [           0.,              0., 1.]])
    T = np.array([[u[0], t[0], n[0]],
                  [u[1], t[1], n[1]],
                  [u[2], t[2], n[2]]])
    invT = np.linalg.inv(T)
    # check if input points are scalar
    if np.isscalar(phi) == True:
        r = 1.
    else:
        r = np.ones(np.shape(phi))
    # convert points on the sphere to cartesian coordinates
    x, y, z = coords.sphere2cart(r, phi, theta)
    pos = np.array([x, y, z]).T
    # apply rotation
    if np.isscalar(phi) == True:
        new_pos = T.dot(Rn.dot(invT.dot(pos)))
        x_new, y_new, z_new = new_pos[0], new_pos[1], new_pos[2]
    else:
        new_pos = np.array([T.dot(Rn.dot(invT.dot(pos[i]))) for i in range(0, len(pos))])
        x_new, y_new, z_new = new_pos[:, 0], new_pos[:, 1], new_pos[:, 2]
    # convert cartesian coordinates back to points on the sphere
    r_new, phi_new, theta_new = coords.cart2sphere(x_new, y_new, z_new)
    return phi_new, theta_new


def usphere_phi_shift(phi, dphi):
    """Shift the longitudinal coordinate.

    Parameters
    ----------
    phi : array
        Longitudinal coordinate.
    dphi : float
        Shift in phi.

    Returns
    -------
    phi_new : array
        Shifted phi coordinates.
    """
    # sanity checks
    assert dphi > -2.*np.pi and dphi < 2.*np.pi, "dphi must be within the range [-2pi, 2pi]."
    # shift phi
    #phi_new = np.copy(phi)
    phi_new = phi
    phi_new += dphi
    if np.isscalar(phi_new) == False:
        condition = np.where(phi_new > 2.*np.pi)[0]
        phi_new[condition] -= 2.*np.pi
        condition = np.where(phi_new < 0.)[0]
        phi_new[condition] += 2.*np.pi
    # scalar case
    else:
        if phi_new > 2.*np.pi:
            phi_new -= 2.*np.pi
        elif phi_new < 0.:
            phi_new += 2.*np.pi
    return phi_new


def usphere_shift(phi, theta, phi_start, theta_start, phi_end, theta_end):
    """Shifted sky coordinates.

    Parameters
    ----------
    phi : array
        Longitudinal coordinates.
    theta : array
        Latitudinal coordinates.
    phi_start : float
        Start phi rotation point.
    theta_start : float
        Start theta rotation point.
    phi_end : float
        End phi rotation point.
    theta_end : float
        End theta rotation point.

    Returns
    -------
    new_phi : array
        Shifted longitudinal coordinates.
    new_theta : array
        Shifted latitudinal coordinates.
    """
    # sanity checks and ranges
    #assert phi_start != phi_end and theta_start != theta_end, "Rotation points must be different."
    assert phi_start >= 0. and phi_start <= 2.*np.pi, "phi_start must lie within [0, 2pi]."
    assert phi_end >= 0. and phi_end <= 2.*np.pi, "phi_end must lie within [0, 2pi]."
    assert theta_start >= 0. and theta_start <= np.pi, "theta_start must lie within [0, pi]."
    assert theta_end >= 0. and theta_end <= np.pi, "theta_end must lie within [0, pi]."
    # apply shift
    #new_phi = np.copy(phi)
    #new_theta = np.copy(theta)
    new_phi = phi
    new_theta = theta
    new_phi = sky_phi_shift(new_phi, phi_end - phi_start)
    if theta_start != theta_end:
        new_phi, new_theta = sky_rotate(new_phi, new_theta, phi_end, theta_end, phi_start=phi_end, theta_start=theta_start)
    return new_phi, new_theta


def usphere_spin(phi, theta, phi_center, theta_center, alpha):
    """Spin coordinates from the longitude and latitude coordinates.

    Parameters
    ----------
    phi : array
        Longitudinal coordinates.
    theta : array
        Latitudinal coordinates.
    phi_center : float
        The longitudinal coordinate defining the axis to spin along.
    theta_center : float
        The latitudinal coordinate defining the axis to spin along.
    alpha : float
        Angle to spin the sky.

    Returns
    -------
    new_phi : array
        Spun longitudinal coordinates.
    new_theta : array
        Spun latitudinal coordinates.
    """
    # sanity checks and ranges
    assert phi_center >= 0. and phi_center <= 2.*np.pi, "phi_center must lie within [0, 2pi]."
    assert theta_center >= 0. and theta_center <= np.pi, "theta_center must lie within [0, pi]."
    assert alpha >= 0. and alpha <= 2.*np.pi, "alpha must lie within [0, 2pi]."
    # apply spin
    # first shift points to the pole
    new_phi, new_theta = sky_shift(phi, theta, phi_center, theta_center, phi_center, 0.)
    # rotate at the pole
    new_phi = sky_phi_shift(new_phi, alpha)
    # shift back to original center
    new_phi, new_theta = sky_shift(new_phi, new_theta, phi_center, 0., phi_center, theta_center)
    return new_phi, new_theta
