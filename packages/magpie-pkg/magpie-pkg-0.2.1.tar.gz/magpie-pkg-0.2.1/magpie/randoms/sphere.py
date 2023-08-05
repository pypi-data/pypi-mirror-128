import numpy as np
import healpy as hp
from . import usphere


def randoms_sphere_r(size, r_min=0., r_max=1.):
    """
    Random radial points for a segment of a sphere (default will give randoms within a unit sphere).

    Parameters
    ----------
    size : int
        Number of randoms to generate.
    r_min : float
        Minimum radius.
    r_max : float
        Maximum radius.

    Returns
    -------
    r : array
        Random r.
    """
    # uniform randoms
    u_r = np.random.random_sample(size)
    # random phi and theta within a given range
    r = ((r_max**3.-r_min**3.)*u_r + r_min**3.)**(1./3.)
    return r


def randoms_sphere(size, r_min=0., r_max=1., phi_min=0., phi_max=2*np.pi, theta_min=0., theta_max=np.pi):
    """Random points inside a sphere (default will give randoms within a unit sphere).
    You can specify the inner and outer radii to get randoms in a shell and the region
    on the sky.

    Note
    ----
    Coordinate convention:
        - phi lies in the range [0, 2pi]
        - theta lies in the rang [0, pi].

    Parameters
    ----------
    size : int
        Number of randoms to generate.
    r_min : float
        Minimum radius.
    r_max : float
        Maximum radius.
    phi_min : float
        Minimum longitude in radians.
    phi_max : float
        Maximum longitude in radians.
    theta_min : float
        Minimum latitude in radians.
    theta_max : float
        Maximum longitude in radians.

    Returns
    -------
    r : array
        Random r.
    phi : array
        Random phi.
    theta : array
        Random theta.
    """
    r = randoms_sphere_r(size, r_min=r_min, r_max=r_max)
    phi, theta = usphere.randoms_usphere(size, phi_min=phi_min, phi_max=phi_max, theta_min=theta_min, theta_max=theta_max)
    return r, phi, theta
