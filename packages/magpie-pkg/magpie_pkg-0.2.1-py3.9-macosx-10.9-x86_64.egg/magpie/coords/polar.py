import numpy as np


def rotate_polar(phi, rotate):
    """Rotates polar coordinates by an input rotation angle.

    Parameters
    ----------
    phi : array
        Angular polar coordinates.
    rotate : float
        Rotation angle.

    Returns
    -------
    rot_phi : array
        Rotated angular polar coordinates.
    """
    assert rotate > 0. and rotate < 2.*np.pi, "Rotation angles must have lie between [0, 2pi]."
    rot_phi = rotate
    cond = np.where(rot_phi >= 2.*np.pi)[0]
    rot_phi[cond] -= 2.*np.pi
    cond = np.where(rot_phi < 0.)[0]
    rot_phi[cond] += 2.*np.pi
    return rot_phi


# this below is not a simple rotation, but a transformation.
def rotate_polar_grid(pedges, f_polar, phi_shift):
    """Rotates polar coordinate grid by phi_shift.

    Parameters
    ----------
    pedges : 2darray
        Polar phi edges.
    f_polar : 2darray
        Polar coordinate gridded data.
    phi_shift : float
        Rotation to be applied, given in radians within a range of 0 and 2pi.

    Returns
    -------
    f_polar_rot : 2darray
        Rotated polar coordinate data.
    """
    assert phi_shift > 0., "phi_shift must be greater than 0."
    assert phi_shift < 2.*np.pi, "phi_shift must be smaller than 2*pi."
    dp = pedges[1] - pedges[0]
    ind_shift = int(np.floor(phi_shift/dp))
    w_shift = phi_shift/dp - ind_shift
    f_polar_rot = np.zeros(np.shape(f_polar))
    if ind_shift != 0:
        f_polar_rot[-ind_shift:] = f_polar[:ind_shift]
        f_polar_rot[:-ind_shift] = f_polar[ind_shift:]
    else:
        f_polar_rot = f_polar
    f_polar_rot[:-1] = w_shift*f_polar_rot[:-1] + (1.-w_shift)*f_polar_rot[1:]
    # check if polar grid has the range 0 to 2pi, if it does wrap the rotation
    if pedges[-1] - pedges[0] == 2.*np.pi:
        f_polar_rot[-1] = w_shift*f_polar_rot[-1] + (1.-w_shift)*f_polar_rot[0]
    else:
        f_polar_rot[-1] *= w_shift
    return f_polar_rot
