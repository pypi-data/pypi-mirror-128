import numpy as np


from . import healpix_index


def _healpix_get_delta(nside):
    """Gets a healpix pixel half length in healpix x and y coordinates.

    Parameters
    ----------
    nside : int
        Healpix Nside.

    Returns
    -------
    delta : float
        Half pixel length in healpix x and y coordinates.
    """
    return np.pi/(4*nside)


def _healpix_top_left(p, nside, steps=10, reverse=False):
    """Returns the boundary on the top lefts ide of a healpix pixel in healpix x
    and y coordinates.

    Parameters
    ----------
    p : int
        Healpix pixel index.
    nside : int
        Healpix Nside.
    steps : int, optional
        Number of steps in the boundary function.
    reverse : bool, optional
        Reverse the order so the output has descending x.

    Returns
    -------
    x : array
        X-coordinates of the top left side of the healpix pixel.
    y : array
        Y-coordinates of the top left side of the healpix pixel.
    """
    xp, yp = healpix_index.healpix_pix2xy(p, nside)
    delta = _healpix_get_delta(nside)
    x = np.linspace(xp-delta, xp, steps)
    y = x - xp + delta + yp
    if reverse == True:
        x, y = x[::-1], y[::-1]
    return x, y


def _healpix_top_right(p, nside, steps=10, reverse=False):
    """Returns the boundary on the top right side of a healpix pixel in healpix x
    and y coordinates.

    Parameters
    ----------
    p : int
        Healpix pixel index.
    nside : int
        Healpix Nside.
    steps : int, optional
        Number of steps in the boundary function.
    reverse : bool, optional
        Reverse the order so the output has descending x.

    Returns
    -------
    x : array
        X-coordinates of the top right side of the healpix pixel.
    y : array
        Y-coordinates of the top right side of the healpix pixel.
    """
    xp, yp = healpix_index.healpix_pix2xy(p, nside)
    delta = _healpix_get_delta(nside)
    x = np.linspace(xp, xp+delta, steps)
    y = - x + xp + delta + yp
    if reverse == True:
        x, y = x[::-1], y[::-1]
    return x, y


def _healpix_bot_left(p, nside, steps=10, reverse=False):
    """Returns the boundary on the bottom left side of a healpix pixel in healpix x
    and y coordinates.

    Parameters
    ----------
    p : int
        Healpix pixel index.
    nside : int
        Healpix Nside.
    steps : int, optional
        Number of steps in the boundary function.
    reverse : bool, optional
        Reverse the order so the output has descending x.

    Returns
    -------
    x : array
        X-coordinates of the bottom left side of the healpix pixel.
    y : array
        Y-coordinates of the bottom left side of the healpix pixel.
    """
    xp, yp = healpix_index.healpix_pix2xy(p, nside)
    delta = _healpix_get_delta(nside)
    x = np.linspace(xp-delta, xp, steps)
    y = - x + xp - delta + yp
    if reverse == True:
        x, y = x[::-1], y[::-1]
    return x, y


def _healpix_bot_right(p, nside, steps=10, reverse=False):
    """Returns the boundary on the bottom right side of a healpix pixel in healpix x
    and y coordinates.

    Parameters
    ----------
    p : int
        Healpix pixel index.
    nside : int
        Healpix Nside.
    steps : int, optional
        Number of steps in the boundary function.
    reverse : bool, optional
        Reverse the order so the output has descending x.

    Returns
    -------
    x : array
        X-coordinates of the bottom right side of the healpix pixel.
    y : array
        Y-coordinates of the bottom right side of the healpix pixel.
    """
    xp, yp = healpix_index.healpix_pix2xy(p, nside)
    delta = _healpix_get_delta(nside)
    x = np.linspace(xp, xp+delta, steps)
    y = x - xp - delta + yp
    if reverse == True:
        x, y = x[::-1], y[::-1]
    return x, y


def _healpix_top(p, nside, steps=20, reverse=False):
    """Returns the top side of a healpix pixel in healpix x and y coordinates.

    Parameters
    ----------
    p : int
        Healpix pixel index.
    nside : int
        Healpix Nside.
    steps : int, optional
        Number of steps for the top function.
    reverse : bool, optional
        Reverse the order so the output has descending x.

    Returns
    -------
    x : array
        X-coordinates of the top side of the healpix pixel.
    y : array
        Y-coordinates of the top side of the healpix pixel.
    """
    size_left = int(steps/2)
    size_right = steps - size_left
    x_left, y_left = _healpix_top_left(p, nside, steps=size_left)
    x_right, y_right = _healpix_top_right(p, nside, steps=size_right)
    x = np.concatenate([x_left, x_right])
    y = np.concatenate([y_left, y_right])
    if reverse == True:
        x, y = x[::-1], y[::-1]
    return x, y


def _healpix_bot(p, nside, steps=20, reverse=False):
    """Returns the bottom side of a healpix pixel in healpix x and y coordinates.

    Parameters
    ----------
    p : int
        Healpix pixel index.
    nside : int
        Healpix Nside.
    steps : int, optional
        Number of steps for the top function.
    reverse : bool, optional
        Reverse the order so the output has descending x.

    Returns
    -------
    x : array
        X-coordinates of the bottom side of the healpix pixel.
    y : array
        Y-coordinates of the bottom side of the healpix pixel.
    """
    size_left = int(steps/2)
    size_right = steps - size_left
    x_left, y_left = _healpix_bot_left(p, nside, steps=size_left)
    x_right, y_right = _healpix_bot_right(p, nside, steps=size_right)
    x = np.concatenate([x_left, x_right])
    y = np.concatenate([y_left, y_right])
    if reverse == True:
        x, y = x[::-1], y[::-1]
    return x, y


def _healpix_boundary(p, nside, steps=40, reverse=False):
    """Returns the boundary of a healpix pixel in healpix x and y coordinates,
    default given in clockwise directions.

    Parameters
    ----------
    p : int
        Healpix pixel index.
    nside : int
        Healpix Nside.
    steps : int, optional
        Number of steps.
    reverse : bool, optional
        Reverse the order so the output is anti-clockwise.

    Returns
    -------
    x : array
        X-coordinates of the boundaries of the healpix pixel.
    y : array
        Y-coordinates of the boundaries of the healpix pixel.
    """
    size_top = int(steps/2)
    size_bot = steps - size_top
    x_top, y_top = _healpix_top(p, nside, steps=size_top)
    x_bot, y_bot = _healpix_bot(p, nside, steps=size_bot, reverse=True)
    x = np.concatenate([x_top, x_bot])
    y = np.concatenate([y_top, y_bot])
    if reverse == True:
        x, y = x[::-1], y[::-1]
    return x, y
