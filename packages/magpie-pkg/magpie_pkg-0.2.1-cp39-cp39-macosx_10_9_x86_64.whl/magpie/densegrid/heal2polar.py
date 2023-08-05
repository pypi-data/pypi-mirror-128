import numpy as np
import healpy as hp

from .. import coords
from .. import polar
from .. import randoms
from .. import utils


class Heal2Polar:
    """Remaps healpix pixels to a 2D polar grid."""

    def __init__(self):
        """Initialises the class."""
        self.nside = None
        self.xedges = None
        self.yedges = None
        self.xmid = None
        self.ymid = None
        self.dx = None
        self.dy = None
        self.x2d = None
        self.y2d = None
        self.center = None
        self.alpha = None
        self.rebin_x = None
        self.rebin_y = None
        self.rebin_xedges = None
        self.rebin_xmid = None
        self.rebin_yedges = None
        self.rebin_ymid = None
        self.rebin_x2d = None
        self.rebin_y2d = None
        self.rebin_xind = None
        self.rebin_yind = None
        self.rebin_pix = None


    def setup_map(self, nside):
        """Setups the HEALPix map.

        Parameters
        ----------
        nside : int
            HEALPix nside.
        """
        assert hp.isnsideok(nside) == True, "nside given is not ok."
        self.nside = nside


    def setup_box(self, x_length, x_grid, center=[0., 0.], alpha=0., y_length=None, y_grid=None,
                  rebin_x=2, rebin_y=2):
        """Setups the polar grid.

        Parameters
        ----------
        x_length : float
            Length of box in radians along the x-axis.
        x_grid : int
            Number of bins along the x-axis.
        center : list
            Center point of the new box grid.
        alpha : float
            Rotation to the polar cap coordinate grid, given in radians within a range
            of 0 and 2pi.
        y_length : float, optional
            Length of box in radians along the y-axis, if None then y_length = x_length.
        y_grid : int
            Number of bins along the y-axis, if None then y_grid = x_grid.
        rebin_x : int
            Rebin factor in the x-axis.
        rebin_y : int
            Rebin factor in the y-axis.
        """
        # sanity checks
        assert x_length >= 0., "x_length must be greater or equal to zero."
        assert x_length <= 2.*np.pi, "x_length must be smaller than 2pi."
        assert x_grid > 0, "x_grid must be greater than zero."
        if y_length is None:
            if x_length > np.pi:
                y_length = np.pi
            else:
                y_length = x_length
        else:
            assert y_length >= 0., "y_length must be greater or equal to zero."
            assert y_length <= np.pi, "y_length must be smaller than pi."
        if y_grid is None:
            y_grid = x_grid
        else:
            assert y_grid > 0, "y_grid must be greater than zero."
        assert len(center) == 2, "center list must have length 2."
        # compute grid info
        self.xedges = np.linspace(-x_length/2., x_length/2., x_grid+1)
        self.yedges = np.linspace(-y_length/2., y_length/2., y_grid+1)
        self.xmid = 0.5*(self.xedges[1:] + self.xedges[:-1])
        self.ymid = 0.5*(self.yedges[1:] + self.yedges[:-1])
        self.dx = self.xmid[1] - self.xmid[0]
        self.dy = self.ymid[1] - self.ymid[0]
        self.x2d, self.y2d = np.meshgrid(self.xmid, self.ymid)
        self.center = center
        self.alpha = alpha
        self.rebin_x = rebin_x
        self.rebin_y = rebin_y
        self.rebin_xedges = np.linspace(self.xedges[0], self.xedges[-1], self.rebin_x*len(self.xmid) + 1)
        self.rebin_xmid = 0.5*(self.rebin_xedges[1:] + self.rebin_xedges[:-1])
        self.rebin_yedges = np.linspace(self.yedges[0], self.yedges[-1], self.rebin_y*len(self.ymid) + 1)
        self.rebin_ymid = 0.5*(self.rebin_yedges[1:] + self.rebin_yedges[:-1])
        self.rebin_x2d, self.rebin_y2d = np.meshgrid(self.rebin_xmid, self.rebin_ymid)
        self.rebin_xind = np.arange(len(self.rebin_xedges)-1)
        self.rebin_yind = np.arange(len(self.rebin_yedges)-1)
        self.rebin_yind, self.rebin_xind = np.meshgrid(self.rebin_xind, self.rebin_yind)
        self.rebin_xind = self.rebin_xind.flatten()
        self.rebin_yind = self.rebin_yind.flatten()
        xx = self.rebin_x2d.flatten()
        yy = self.rebin_y2d.flatten()
        yy = np.pi/2. - yy
        if self.alpha != 0.:
            xx, yy = coords.usphere_spin(xx, yy, 0., np.pi/2., self.alpha)
        xx, yy = coords.usphere_shift(xx, yy, 0., np.pi/2., self.center[0], self.center[1])
        self.rebin_pix = hp.ang2pix(self.nside, yy, xx)


    def _remap(self, f):
        """Remaps 2d grid data f onto polar coordinate grid.

        Parameters
        ----------
        f : array
            HEALPix input map.

        Returns
        -------
        f_box : 2darray
            Remapped 2d data onto polar coordinate grid.
        """
        f_box_highres = np.zeros(np.shape(self.rebin_x2d))
        f_box_highres[self.rebin_xind, self.rebin_yind] = f[self.rebin_pix]
        dx = self.rebin_xedges[1] - self.rebin_xedges[0]
        area = np.array([coords.sky_area(0., dx, self.rebin_yedges[i]+np.pi/2., self.rebin_yedges[i+1]+np.pi/2.) for i in range(0, len(self.rebin_yedges)-1)])
        y_bin_weights = area
        _, y_bin_weights_2d = np.meshgrid(self.rebin_xmid, y_bin_weights)
        f_box_highres *= y_bin_weights_2d
        f_box = np.sum(f_box_highres.reshape(len(self.x2d), self.rebin_x, len(self.rebin_x2d[0])), axis=1)
        f_box = np.mean(f_box.reshape(len(self.x2d), len(self.x2d[0]), self.rebin_y), axis=2)
        y_bin_weights_2d = np.sum(y_bin_weights_2d.reshape(len(self.x2d), self.rebin_x, len(self.rebin_y2d[0])), axis=1)
        y_bin_weights_2d = np.mean(y_bin_weights_2d.reshape(len(self.x2d), len(self.x2d[0]), self.rebin_y), axis=2)
        f_box /= y_bin_weights_2d
        return f_box


    def remap(self, f, w=None, verbose=True):
        """Remaps 2d grid data f onto polar coordinate grid.

        Parameters
        ----------
        f : array
            HEALPix input map.
        w : array
            HEALPix input weight.
        verbose : bool
            This does nothing. This is here simply so that no errors occur when
            switching from Monte Carlo weighted remapping to the dense grid remapping.

        Returns
        -------
        f_box : 2darray
            Remapped 2d data onto polar coordinate grid.
        """
        if w is None:
            f_box = self._remap(f)
        else:
            f_box = self._remap(f*w)/self._remap(w)
        return f_box


    def clean(self):
        """Cleans by reinitialising the class."""
        self.__init__()
