import numpy as np


def get_box(xmin, xmax, ymin, ymax, divisions=1):
    """Returns the coordinates of the perimeter of a box.

    Parameters
    ----------
    xmin : float
        Minimum x-value.
    xmax : float
        Maximum x-value.
    ymin : float
        Minimum y-value.
    ymax : float
        Maximum y-value.
    divisions : int, optional
        Number of divisions across each line segment.
    """
    x = []
    y = []
    xx = np.linspace(xmin, xmax, divisions+1)
    yy = np.ones(divisions+1)*ymin
    x = xx[:-1]
    y = yy[:-1]
    xx = np.ones(divisions+1)*xmax
    yy = np.linspace(ymin, ymax, divisions+1)
    x = np.concatenate([x, xx[:-1]])
    y = np.concatenate([y, yy[:-1]])
    xx = np.linspace(xmax, xmin, divisions+1)
    yy = np.ones(divisions+1)*ymax
    x = np.concatenate([x, xx[:-1]])
    y = np.concatenate([y, yy[:-1]])
    xx = np.ones(divisions+1)*xmin
    yy = np.linspace(ymax, ymin, divisions+1)
    x = np.concatenate([x, xx])
    y = np.concatenate([y, yy])
    return x, y


def get_circle(radius, center=[0., 0.], length=100):
    """Returns the coordinates of the perimeter of a box.

    Parameters
    ----------
    radius : float
        Radius of the circle.
    center : list, optional
        Central x and y coordinate of the circle.
    length : int, optional
        Length of the circle coordinates.
    """
    phi = np.zeros(length)
    phi[:-1] = np.linspace(0., 2.*np.pi, length)[:-1]
    r = np.ones(length)*radius
    x = r*np.cos(phi)
    y = r*np.sin(phi)
    x += center[0]
    y += center[0]
    return x, y


def get_cube(xmin, xmax, ymin, ymax, zmin, zmax, divisions=100, return_nearest=False, center=[0., 0., 0.]):
    """Returns 3D coordinates for a cube.

    Parameters
    ----------
    xmin : float
        Minimum x value.
    xmax : float
        Maximum x value.
    ymin : float
        Minimum y value.
    ymax : float
        Maximum y value.
    zmin : float
        Minimum z value.
    zmax : float
        Maximum z value.
    divisions : int, optional
        Number of divisions in each line element.
    return_nearest : bool, optional
        If True only the lines for the nearest or visible faces from a defined center will be outputed.
    center : list, optional
        Coordinate center used for return_nearest=True
    """
    xmin_arr = xmin*np.ones(divisions)
    xmax_arr = xmax*np.ones(divisions)
    ymin_arr = ymin*np.ones(divisions)
    ymax_arr = ymax*np.ones(divisions)
    zmin_arr = zmin*np.ones(divisions)
    zmax_arr = zmax*np.ones(divisions)
    x_arr = np.linspace(xmin, xmax, divisions)
    y_arr = np.linspace(ymin, ymax, divisions)
    z_arr = np.linspace(zmin, zmax, divisions)
    x = np.array([x_arr, x_arr, xmin_arr, xmax_arr, x_arr, x_arr, xmin_arr, xmax_arr, xmin_arr, xmax_arr, xmin_arr, xmax_arr])
    y = np.array([ymin_arr, ymax_arr, y_arr, y_arr, ymin_arr, ymax_arr, y_arr, y_arr, ymin_arr, ymin_arr, ymax_arr, ymax_arr])
    z = np.array([zmin_arr, zmin_arr, zmin_arr, zmin_arr, zmax_arr, zmax_arr, zmax_arr, zmax_arr, z_arr, z_arr, z_arr, z_arr])
    if return_nearest == True:
        corners = np.array([[xmin, ymin, zmin], [xmin, ymin, zmax], [xmin, ymax, zmin], [xmin, ymax, zmax],
                            [xmax, ymin, zmin], [xmax, ymin, zmax], [xmax, ymax, zmin], [xmax, ymax, zmax]])
        xc, yc, zc = corners[:, 0], corners[:, 1], corners[:, 2]
        dist = np.sqrt((xc - center[0])**2. + (yc - center[1])**2. + (zc - center[2])**2.)
        indmax = np.argmax(dist)
        remove_corner = []
        for i in range(0, len(corners)):
            xx = np.linspace(0., 1., 100)*(xc[i] - center[0]) + center[0]
            yy = np.linspace(0., 1., 100)*(yc[i] - center[1]) + center[1]
            zz = np.linspace(0., 1., 100)*(zc[i] - center[2]) + center[2]
            condition = np.where((xx > xmin) & (xx < xmax) & (yy > ymin) & (yy < ymax) & (zz > zmin) & (zz < zmax))[0]
            if len(condition) == 0:
                remove_corner.append(False)
            else:
                remove_corner.append(True)
        xnew = []
        ynew = []
        znew = []
        for i in range(0, len(x)):
            x1, y1, z1 = x[i][0], y[i][0], z[i][0]
            x2, y2, z2 = x[i][-1], y[i][-1], z[i][-1]
            dist1 = np.sqrt((xc - x1)**2. + (yc - y1)**2. + (zc - z1)**2.)
            dist2 = np.sqrt((xc - x2)**2. + (yc - y2)**2. + (zc - z2)**2.)
            remove_corner1 = remove_corner[np.argmin(dist1)]
            remove_corner2 = remove_corner[np.argmin(dist2)]
            if remove_corner1 == True or remove_corner2 == True:
                remove = True
            else:
                remove = False
            if remove == False:
                xnew.append(x[i])
                ynew.append(y[i])
                znew.append(z[i])
        xnew = np.array(xnew)
        ynew = np.array(ynew)
        znew = np.array(znew)
        x, y, z = xnew, ynew, znew
    return x, y, z
