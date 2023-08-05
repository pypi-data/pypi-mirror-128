import numpy as np
import healpy as hp

from .. import coords
from .. import polar
from .. import randoms
from .. import utils


class Heal2Polar:
    """Remaps pixels given a HEALPix map to a polar cap grid."""


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
        self.ind_pixs = None
        self.ind_ws = None


    def setup_map(self, nside):
        """Setups the HEALPix map.

        Parameters
        ----------
        nside : int
            HEALPix nside.
        """
        assert hp.isnsideok(nside) == True, "nside given is not ok."
        self.nside = nside


    def setup_box(self, x_length, x_grid, center=[0., 0.], alpha=0., y_length=None, y_grid=None):
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


    def get_weights(self, mc_size=10000, verbose=True):
        """Calculates Monte Carlo pixel weights for remapping from cartesian grid
        to box coordinate grid.

        Parameters
        ----------
        mc_size : int
            Size of the Monte Carlo random points for calculating weights from Monte
            Carlo integration.
        verbose : bool
            If true will output a progress bar.
        """
        assert mc_size > 1, "mc_size must be greater than 1, ideally greater than 100."
        ind_pixs = []
        ind_ws = []
        for i in range(0, len(self.x2d)):
            _ind_pixs = []
            _ind_ws = []
            for j in range(0, len(self.x2d[0])):
                x_min, x_max = self.xedges[j], self.xedges[j+1]
                y_max, y_min = self.yedges[i], self.yedges[i+1]
                y_min = np.pi/2. - y_min
                y_max = np.pi/2. - y_max
                x_rand, y_rand = randoms.randoms_sky(mc_size, phi_min=x_min, phi_max=x_max, theta_min=y_min, theta_max=y_max)
                if self.alpha != 0.:
                    x_rand, y_rand = coords.usphere_spin(x_rand, y_rand, 0., np.pi/2., self.alpha)
                x_rand, y_rand = coords.usphere_shift(x_rand, y_rand, 0., np.pi/2., self.center[0], self.center[1])
                pix_rand = hp.ang2pix(self.nside, y_rand, x_rand)
                pix_uniq, pix_counts = np.unique(pix_rand, return_counts=True)
                ind_pix = pix_uniq
                ind_w = (pix_counts.astype('float'))/float(mc_size)
                _ind_pixs.append(ind_pix)
                _ind_ws.append(ind_w)
            ind_pixs.append(np.array(_ind_pixs, dtype=object))
            ind_ws.append(np.array(_ind_ws, dtype=object))
            if verbose == True:
                utils.progress_bar(i, len(self.x2d), explanation='Calculating weights')
        self.ind_pixs = np.array(ind_pixs, dtype=object)
        self.ind_ws = np.array(ind_ws, dtype=object)


    def remap(self, f, w=None, verbose=True):
        """Remaps HEALPix map f into polar coordinate grid.

        Parameters
        ----------
        f : array
            HEALPix input map
        w : array
            HEALPix weight map.
        verbose : bool
            If true will output a progress bar.

        Returns
        -------
        f_polar : 2darray
            Remapped 2d data onto polar cap coordinate grid.
        """
        assert len(f) == hp.nside2npix(self.nside), "HEALPix map f is not the correct nside."
        if w is not None:
            assert np.shape(w) ==hp.nside2npix(self.nside), "HEALPix weight map w is not the correct nside."
        f_box = np.zeros(np.shape(self.x2d))
        for i in range(0, len(self.x2d)):
            for j in range(0, len(self.x2d[0])):
                if w is None:
                    if np.sum(self.ind_ws[i, j]) != 0.:
                        f_box[i, j] = np.sum(self.ind_ws[i, j]*f[self.ind_pixs[i, j]])
                        f_box[i, j] /= np.sum(self.ind_ws[i, j])
                    else:
                        f_box[i, j] = np.nan
                else:
                    if np.sum(self.ind_ws[i, j]) != 0.:
                        f_box[i, j] = np.sum(self.ind_ws[i, j]*w[self.ind_pixs[i, j]]*f[self.ind_pixs[i, j]])
                        f_box[i, j] /= np.sum(self.ind_ws[i, j]*w[self.ind_pixs[i, j]])
                    else:
                        f_box[i, j] = np.nan
            if verbose == True:
                utils.progress_bar(i, len(self.x2d), explanation='Remapping')
        return f_box


    def clean(self):
        """Cleans by reinitialising the class."""
        self.__init__()
