import numpy as np


def healpix_pix2ij(p, Nside):
    """Returns the healpix ring i and pixel along the ring j.

    Parameters
    ----------
    p : int
        Healpix pixel index.
    Nside : int
        Healpix Nside.

    Returns
    -------
    ringi : int
        Pixel ring index.
    ringj : int
        Pixel index along each ring.
    """
    if np.isscalar(p) == True:
        if p <= 2*Nside*(Nside+1):
            # top polar cap
            ph = (p+1)/2
            i = np.floor(np.sqrt(ph - np.sqrt(np.floor(ph))))+1
            j = p + 1 - 2*i*(i-1)
            ringi, ringj = int(i), int(j)
        elif p > 2*Nside*(Nside+1) and p < 2*Nside*(5*Nside-1):
            # equatorial sector
            pd = p - 2*Nside*(Nside-1)
            i = np.floor(pd/(4*Nside)) + Nside
            j = (pd % (4*Nside)) + 1
            ringi, ringj = int(i), int(j)
        elif p >= 2*Nside*(5*Nside-1) and p <= 12*Nside**2:
            # bottom polar cap
            ph = (12*Nside**2 - p)/2
            i = np.floor(np.sqrt(ph-np.sqrt(np.floor(ph))))+1
            j = p + 2*i*(i + 1) + 1 - 12*Nside**2
            ringi, ringj = int(4*Nside-i), int(j)
    else:
        i, j = np.zeros(len(p)), np.zeros(len(p))
        # top polar cap
        cond = np.where(p <= 2*Nside*(Nside+1))[0]
        ph = (p[cond]+1)/2
        i[cond] = np.floor(np.sqrt(ph - np.sqrt(np.floor(ph)))) + 1
        j[cond] = p[cond] + 1 - 2*i[cond]*(i[cond]-1)
        # equatorial sector
        cond = np.where((p > 2*Nside*(Nside+1)) & (p < 2*Nside*(5*Nside-1)))[0]
        pd = p[cond] - 2*Nside*(Nside-1)
        i[cond] = np.floor(pd/(4*Nside)) + Nside
        j[cond] = (pd % (4*Nside)) + 1
        # bottom polar cap
        cond = np.where((p >= 2*Nside*(5*Nside-1)) & (p <= 12*Nside**2))[0]
        ph = (12*Nside**2 - p[cond])/2
        i[cond] = np.floor(np.sqrt(ph-np.sqrt(np.floor(ph)))) + 1
        j[cond] = p[cond] + 2*i[cond]*(i[cond] + 1) + 1 - 12*Nside**2
        i[cond] = 4*Nside - i[cond]
        ringi = i.astype('int')
        ringj = j.astype('int')
    return ringi, ringj


def healpix_ij2pix(ringi, ringj, Nside):
    """Returns the healpix ring i and pixel along the ring j.

    Parameters
    ----------
    ringi : int
        Pixel ring index.
    ringj : int
        Pixel index along each ring.
    Nside : int
        Healpix Nside.

    Returns
    -------
    p : int
        Healpix pixel index.
    """
    if np.isscalar(ringi) == True:
        if ringi <= Nside:
            # top polar cap
            p = 2*ringi*(ringi - 1) + ringj - 1
        elif ringi > Nside and ringi < 3*Nside:
            # equatorial sector
            p = 4*Nside*(ringi - Nside) + ringj - 1 + 2*Nside*(Nside - 1)
        elif ringi >= 3*Nside:
            # bottom polar cap
            i = 4*Nside - ringi
            p = 12*Nside**2 + ringj - 2*i*(i + 1) - 1
        p = int(p)
    else:
        p = np.zeros(len(ringi))
        # top polar cap
        cond = np.where(ringi <= Nside)[0]
        p[cond] = 2*ringi[cond]*(ringi[cond] - 1) + ringj[cond] - 1
        # equatorial sector
        cond = np.where((ringi > Nside) & (ringi < 3*Nside))[0]
        p[cond] = 4*Nside*(ringi[cond] - Nside) + ringj[cond] - 1 + 2*Nside*(Nside - 1)
        # bottom polar cap
        cond = np.where(ringi >= 3*Nside)[0]
        i = 4*Nside - ringi[cond]
        p[cond] = 12*Nside**2 + ringj[cond] - 2*i*(i + 1) - 1
        p = p.astype('int')
    return p


def healpix_i2id(ringi, Nside):
    """Converts ringi to idash.

    Parameters
    ----------
    ringi : int
        Pixel ring index.
    Nside : int
        Healpix Nside.

    Returns
    -------
    idash : int
        Alternate pixel index along each ring. This is for pixel transformations
        as this maps exactly to healpix y without a factor.
    """
    idash = Nside - ringi/2
    return idash


def healpix_j2jd(ringi, ringj, Nside):
    """Converts ringj to jdash.

    Parameters
    ----------
    ringi : int
        Pixel ring index.
    ringj : int
        Pixel index along each ring.
    Nside : int
        Healpix Nside.

    Returns
    -------
    jdash : int
        Alternate pixel index along each ring. This is for pixel transformations
        as this maps exactly to healpix x without a factor.
    """
    if np.isscalar(ringi) == True:
        # North Polar Cap
        if ringi <= Nside:
            jlen = 4*ringi
            k = np.floor(4*(ringj-1)/jlen)
            x0 = int(Nside/2) + Nside*k
            if Nside % 2 == 0:
                x0 = x0 - 0.5*(ringi-1)
            else:
                x0 = x0 - 0.5*(ringi) + 1
            jdash = x0 + ((ringj - 1) % (jlen/4))

        # Equatorial Segment
        elif ringi > Nside and ringi < 3*Nside:
            if Nside % 2 == 0:
                x0 = 0.5*((ringi+1) % 2)
            else:
                x0 = 0.5*(ringi % 2)
            jdash = x0 + ringj - 1.

        # South Polar Cap
        elif ringi >= 3*Nside:
            jlen = 4*(4*Nside - ringi)
            k =  np.floor(4*(ringj-1)/jlen)
            x0 = int(Nside/2) + Nside*k
            if Nside % 2 == 0:
                x0 = x0 - 0.5*(4*Nside-ringi-1)
            else:
                x0 = x0 - 0.5*(4*Nside-ringi) + 1
            jdash = x0 + ((ringj - 1) % (jlen/4))

    else:

        jdash = np.zeros(len(ringi))

        # North Polar Cap
        cond = np.where(ringi <= Nside)[0]

        jlen = 4*ringi[cond]
        k = np.floor(4*(ringj[cond]-1)/jlen)
        x0 = int(Nside/2) + Nside*k
        if Nside % 2 == 0:
            x0 = x0 - 0.5*(ringi[cond]-1)
        else:
            x0 = x0 - 0.5*(ringi[cond]) + 1
        jdash[cond] = x0 + ((ringj[cond]-1) % (jlen/4))

        # Equatorial Segment
        cond = np.where((ringi > Nside) & (ringi < 3*Nside))[0]

        if Nside % 2 == 0:
            x0 = 0.5*((ringi[cond]+1) % 2)
        else:
            x0 = 0.5*(ringi[cond] % 2)
        jdash[cond] = x0 + ringj[cond] - 1.

        # South Polar Cap
        cond = np.where(ringi >= 3*Nside)[0]

        jlen = 4*(4*Nside - ringi[cond])
        k = np.floor(4*(ringj[cond]-1)/jlen)
        x0 = int(Nside/2) + Nside*k
        if Nside % 2 == 0:
            x0 = x0 - 0.5*(4*Nside-ringi[cond]-1)
        else:
            x0 = x0 - 0.5*(4*Nside-ringi[cond]) + 1
        jdash[cond] = x0 + ((ringj[cond]-1) % (jlen/4))

    return jdash


def healpix_ijd2ijs(idash, jdash, Nside):
    """Converts from healpix i and j dash to i and j star, which is useful for
    finding neighbours.

    Parameters
    ----------
    idash : int
        Alternate pixel index along each ring. This is for pixel transformations
        as this maps exactly to healpix y without a factor.
    jdash : int
        Alternate pixel index along each ring. This is for pixel transformations
        as this maps exactly to healpix x without a factor.

    Returns
    -------
    istar : array
        Healpix integer i star index.
    jstar : array
        Healpix integer i star index.
    """
    istar = jdash - idash + Nside/2
    jstar = jdash + idash + Nside/2
    istar -= 0.5
    istar = istar.astype('int')
    jstar -= 0.5
    jstar = jstar.astype('int')
    return istar, jstar


def healpix_ijs2ijd(istar, jstar, Nside):
    """Converts from healpix i and j star to i and j dash, which is useful for
    finding neighbours.

    Parameters
    ----------
    istar : array
        Healpix integer i star index.
    jstar : array
        Healpix integer i star index.

    Returns
    -------
    idash : int
        Alternate pixel index along each ring. This is for pixel transformations
        as this maps exactly to healpix y without a factor.
    jdash : int
        Alternate pixel index along each ring. This is for pixel transformations
        as this maps exactly to healpix x without a factor.
    """
    istar = istar.astype('float') + 0.5
    jstar = jstar.astype('float') + 0.5
    jdash = (istar + jstar - Nside)/2
    idash = (jstar - istar)/2
    return idash, jdash


def healpix_ijs_neighbours(istar, jstar, Nside):
    """Gets the healpix i, jstar neighbours for a single healpix pixel.

    Parameters
    ----------
    istar : array
        Healpix integer i star index.
    jstar : array
        Healpix integer i star index.
    Nside : int
        Healpix Nside.

    Returns
    -------
    istar_neigh : array
        Neighbour healpix integer i star index.
    jstar_neigh : array
        Neighbour healpix integer j star index.
    """
    if jstar - istar + 1 == 2*Nside:
        istar_neigh = [istar, istar + 1, istar + 1, istar + Nside, istar + Nside, istar - Nside, istar + 1 - Nside, istar+2*Nside]
        jstar_neigh = [jstar - 1,  jstar - 1, jstar, jstar - 1 + Nside, jstar + Nside, jstar - Nside, jstar - Nside, jstar+2*Nside]
    elif istar - jstar + 1 == 2*Nside:
        istar_neigh = [istar, istar - 1, istar - 1, istar - Nside, istar - Nside, istar + Nside, istar - 1 + Nside, istar-2*Nside]
        jstar_neigh = [jstar + 1,  jstar + 1, jstar, jstar + 1 - Nside, jstar - Nside, jstar + Nside, jstar + Nside, jstar-2*Nside]
    elif jstar - istar + 1 == Nside and istar % Nside == 0:
        istar_neigh = [istar - 1, istar, istar + 1,  istar - 1, istar + 1, istar, istar + 1]
        jstar_neigh = [jstar - 1, jstar - 1, jstar - 1, jstar, jstar, jstar + 1, jstar + 1]
    elif istar - jstar + 1 == Nside and jstar % Nside == 0:
        istar_neigh = [istar - 1, istar, istar - 1, istar + 1, istar - 1, istar, istar + 1]
        jstar_neigh = [jstar - 1, jstar - 1, jstar, jstar, jstar + 1, jstar + 1, jstar + 1]
    elif istar % Nside == 0 and jstar + 1 - Nside*(np.floor(istar/Nside) + 1) > 0:
        istar_neigh = [istar, istar + 1, istar + 1, istar, istar + 1,
                     istar - ((jstar+1)-Nside*np.floor(jstar/Nside)),
                     istar - ((jstar)-Nside*np.floor(jstar/Nside)),
                     istar - ((jstar-1)-Nside*np.floor(jstar/Nside))]
        jstar_neigh = [jstar - 1, jstar - 1, jstar, jstar + 1, jstar + 1,
                     Nside*np.floor(jstar/Nside)-1,
                     Nside*np.floor(jstar/Nside)-1,
                     Nside*np.floor(jstar/Nside)-1]
    elif jstar % Nside == 0 and istar + 1 - Nside*(np.floor(jstar/Nside) + 1) > 0:
        jstar_neigh = [jstar, jstar + 1, jstar + 1, jstar, jstar + 1,
                     jstar - ((istar+2)-Nside*np.floor(istar/Nside)),
                     jstar - ((istar+1)-Nside*np.floor(istar/Nside)),
                     jstar - ((istar)-Nside*np.floor(istar/Nside))]
        istar_neigh = [istar - 1, istar - 1, istar, istar + 1, istar + 1,
                     Nside*np.floor(istar/Nside)-1,
                     Nside*np.floor(istar/Nside)-1,
                     Nside*np.floor(istar/Nside)-1]
    elif (jstar + 1 - Nside) % Nside == 0 and jstar + 1 - Nside*(np.floor(istar/Nside) + 1) > 0:
        jstar_neigh = [jstar, jstar - 1, jstar - 1, jstar, jstar - 1,
                     jstar + Nside*(np.floor(istar/Nside)+1)-istar,
                     jstar + Nside*(np.floor(istar/Nside)+1)-istar-1,
                     jstar + Nside*(np.floor(istar/Nside)+1)-istar+1]
        istar_neigh = [istar - 1, istar - 1, istar, istar + 1, istar + 1,
                     Nside*(np.floor(istar/Nside)+1),
                     Nside*(np.floor(istar/Nside)+1),
                     Nside*(np.floor(istar/Nside)+1)]
    elif (istar + 1 - Nside) % Nside == 0 and istar + 1 - Nside*(np.floor(jstar/Nside) + 1) > 0:
        istar_neigh = [istar, istar - 1, istar - 1, istar, istar - 1,
                     istar + Nside*(np.floor(jstar/Nside)+1)-jstar,
                     istar + Nside*(np.floor(jstar/Nside)+1)-jstar-1,
                     istar + Nside*(np.floor(jstar/Nside)+1)-jstar+1]
        jstar_neigh = [jstar - 1, jstar - 1, jstar, jstar + 1, jstar + 1,
                     Nside*(np.floor(jstar/Nside)+1),
                     Nside*(np.floor(jstar/Nside)+1),
                     Nside*(np.floor(jstar/Nside)+1)]
    else:
        istar_neigh = [istar - 1, istar, istar + 1, istar - 1, istar + 1, istar - 1, istar, istar + 1]
        jstar_neigh = [jstar - 1, jstar - 1, jstar - 1, jstar, jstar, jstar + 1, jstar + 1, jstar + 1]

    istar_neigh = np.array(istar_neigh)
    jstar_neigh = np.array(jstar_neigh)

    cond = np.where(istar_neigh + jstar_neigh > 9*Nside-1)[0]
    istar_neigh[cond] = istar_neigh[cond] - 4*Nside
    jstar_neigh[cond] = jstar_neigh[cond] - 4*Nside

    cond = np.where(istar_neigh + jstar_neigh < Nside-1)[0]
    istar_neigh[cond] = istar_neigh[cond] + 4*Nside
    jstar_neigh[cond] = jstar_neigh[cond] + 4*Nside

    istar_neigh = np.unique(istar_neigh)
    jstar_neigh = np.unique(jstar_neigh)
    return istar_neigh, jstar_neigh


def healpix_ij2xy(ringi, ringj, Nside):
    """Conversion of healpix ring i and j to healpix x and y.

    Parameters
    ----------
    ringi : int
        Pixel ring index.
    ringj : int
        Pixel index along each ring.
    Nside : int
        Healpix Nside.

    Returns
    -------
    healx : array
        Healpix x coordinates.
    healy : array
        Healpix y coordinates.
    """
    jdash = healpix_j2jd(ringi, ringj, Nside)
    idash = healpix_i2id(ringi, Nside)
    healx = jdash * np.pi/(2*Nside)
    healy = idash * np.pi/(2*Nside)
    return healx, healy


def healpix_pix2xy(p, Nside):
    """Returns the healpix ring i and pixel along the ring j.

    Parameters
    ----------
    p : int
        Healpix pixel index.
    Nside : int
        Healpix Nside.

    Returns
    -------
    healx : array
        Healpix x coordinates.
    healy : array
        Healpix y coordinates.
    """
    ringi, ringj = healpix_pix2ij(p, Nside)
    healx, healy = healpix_ij2xy(ringi, ringj, Nside)
    return healx, healy
