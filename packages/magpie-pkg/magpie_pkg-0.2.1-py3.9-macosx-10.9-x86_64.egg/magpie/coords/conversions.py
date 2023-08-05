import numpy as np


def cart2polar(x, y, center=[0., 0.]):
    """Returns the polar coordinates for a given set of cartesian coordinates.

    Parameters
    ----------
    x : array
        x coordinates.
    y : array
        y coordinates.
    center : list
        Center point of polar coordinate grid.

    Returns
    -------
    r : array
        Radial coordinate.
    phi : array
        Phi coordinate.
    """
    r = np.sqrt((x-center[0])**2. + (y-center[1])**2.)
    phi = np.arctan2(y-center[1], x-center[0])
    if np.isscalar(phi) == True:
        if phi < 0.:
            phi += 2.*np.pi
    else:
        condition = np.where(phi < 0.)
        phi[condition] += 2.*np.pi
    return r, phi


def polar2cart(r, phi, center=[0., 0.]):
    """Return cartesian coordinates for a given set of polar coordinates.

    Parameters
    ----------
    r : array
        Radial coordinate.
    phi : array
        Phi coordinate.
    center : list
        Center point of polar coordinate grid.

    Returns
    -------
    x : array
        x coordinate
    y : array
        y coordinate
    """
    x = r*np.cos(phi) + center[0]
    y = r*np.sin(phi) + center[1]
    return x, y


def cart2sphere(x, y, z, center=[0., 0., 0.]):
    """Return polar coordinates for a given set of cartesian coordinates.

    Parameters
    ----------
    x : array
        x coordinate
    y : array
        y coordinate
    center : list
        Center point of polar coordinate grid.Coordin

    Returns
    -------
    r : array
        Radial coordinates.
    phi : array
        Phi coordinates [0, 2pi].
    theta : array
        Theta coordinates [0, pi].
    """
    r = np.sqrt((x-center[0])**2. + (y-center[1])**2. + (z-center[2])**2.)
    phi = np.arctan2(y-center[1], x-center[0])
    if np.isscalar(phi) == True:
        if phi < 0.:
            phi += 2.*np.pi
        if r != 0.:
            theta = np.arccos((z-center[2])/r)
        else:
            theta = 0.
    else:
        condition = np.where(phi < 0.)
        phi[condition] += 2.*np.pi
        theta = np.zeros(len(phi))
        condition = np.where(r != 0.)[0]
        theta[condition] = np.arccos((z[condition]-center[2])/r[condition])
    return r, phi, theta


def sphere2cart(r, phi, theta, center=[0., 0., 0.]):
    """Converts spherical polar coordinates into cartesian coordinates.

    Parameters
    ----------
    r : array
        Radial distance.
    phi : array
        Longitudinal coordinates (radians = [0, 2pi]).
    theta : array
        Latitude coordinates (radians = [0, pi]).
    center : list
        Center point of spherical polar coordinate grid.

    Returns
    -------
    x, y, z : array
        Euclidean coordinates.
    """
    phi = np.copy(phi)
    theta = np.copy(theta)
    x = r * np.cos(phi) * np.sin(theta)
    y = r * np.sin(phi) * np.sin(theta)
    z = r * np.cos(theta)
    x += center[0]
    y += center[1]
    z += center[2]
    return x, y, z


def ortho2cart(x, y, r=1., fill_value=np.nan):
    """Orthographic projection to cartesian coordinates.

    Parameters
    ----------
    x : array
        X value in the orthographic projection.
    y : array
        Y value in the orthographic projection.
    r : float
        Radius of the sphere.
    fill_value : float
        Fill values outside the sphere with this value.

    Returns
    -------
    z : array
        Returns the z value of the cartesian coordinates.
    """
    xy = x**2. + y**2.
    if np.isscalar(x) == True:
        if xy < r**2.:
            z = np.sqrt(r**2 - xy)
        else:
            z = fill_value
    else:
        z = np.ones(np.shape(x)) * fill_value
        condition = np.where(xy < r**2.)
        z[condition] = np.sqrt(r**2. - xy[condition])
    return z
