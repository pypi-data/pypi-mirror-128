import numpy as np


def healpix_xy2ang(healx, healy):
    """Converts from healpix x and y to unit sphere phi and theta

    Parameters
    ----------
    healx : array
        Healpix x coordinates.
    healy : array
        Healpix y coordinates.

    Returns
    -------
    phi : array
        Phi coordinates [0, 2pi].
    theta : array
        Theta coordinates [0, pi].
    """
    if np.isscalar(healx) == True:
        if abs(healy) <= np.pi/4:
            z = 8*healy/(3*np.pi)
            theta = np.arccos(z)
            phi = healx
        else:
            sigz = 4*healy/np.pi
            z = np.sign(sigz)*(1-(1/3)*(2-abs(sigz))**2)
            theta = np.arccos(z)
            siga = abs(sigz)-1
            k = np.floor(2*healx/np.pi)
            if siga == 1.:
                phi = 0.
            else:
                phi = (healx - (np.pi/4)*siga*(2*k+1)) / (1-siga)
    else:
        phi, theta = np.zeros(len(healx)), np.zeros(len(healx))
        cond = np.where((abs(healy) <= np.pi/4))[0]
        z = 8*healy[cond]/(3*np.pi)
        theta[cond] = np.arccos(z)
        phi[cond] = healx[cond]
        cond = np.where((abs(healy) > np.pi/4))[0]
        sigz = 4*healy[cond]/np.pi
        z = np.sign(sigz)*(1-(1/3)*(2-abs(sigz))**2)
        theta[cond] = np.arccos(z)
        siga = abs(sigz)-1
        k = np.floor(2*healx[cond]/np.pi)
        if any(siga == 1.) == False:
            phi[cond] = (healx[cond] - (np.pi/4)*siga*(2*k+1)) / (1-siga)
        else:
            cond1 = np.where(siga == 1.)[0]
            phi[cond[cond1]] = 0.
            cond2 = np.where(siga != 1.)[0]
            phi[cond[cond2]] = (healx[cond[cond2]] - (np.pi/4)*siga[cond2]*(2*k[cond2]+1)) / (1-siga[cond2])
    return phi, theta


def healpix_ang2xy(phi, theta):
    """Converts from healpix x and y to unit sphere phi and theta

    Parameters
    ----------
    phi : array
        Phi coordinates [0, 2pi].
    theta : array
        Theta coordinates [0, pi].

    Returns
    -------
    healx : array
        Healpix x coordinates.
    healy : array
        Healpix y coordinates.
    """
    if np.isscalar(phi) == True:
        z = np.cos(theta)
        if abs(z) <= 2/3:
            healx = phi
            healy = (3*np.pi/8)*np.cos(theta)
        elif abs(z) > 2/3:
            sigz = np.sign(z)*(2 - np.sqrt(3*(1-abs(z))))
            phit = phi % (np.pi/2)
            siga = abs(sigz) - 1
            healx = phi - siga*(phit - np.pi/4)
            healy = np.pi * sigz / 4
    else:
        z = np.cos(theta)
        healx = np.zeros(len(phi))
        healy = np.zeros(len(theta))
        cond = np.where(abs(z) <= 2/3)[0]
        healx[cond] = phi[cond]
        healy[cond] = (3*np.pi/8)*np.cos(theta[cond])
        cond = np.where(abs(z) > 2/3)[0]
        sigz = np.sign(z[cond])*(2 - np.sqrt(3*(1-abs(z[cond]))))
        phit = phi[cond] % (np.pi/2)
        siga = abs(sigz) - 1
        healx[cond] = phi[cond] - siga*(phit - np.pi/4)
        healy[cond] = np.pi * sigz / 4
    return healx, healy
