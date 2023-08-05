import numpy as np
import healpy as hp

from .. import coords
from .. import polar
from .. import randoms
from .. import utils


class Heal2Ring:
    """Remaps pixels given on 2D grid to polar grid."""


    def __init__(self):
        """Initialises the class."""
        self.nside = None
        self.alpha_edges = None
        self.beta_edges = None
        self.alpha_mid = None
        self.beta_mid = None
        self.dalpha = None
        self.dbeta = None
        self.alpha2d = None
        self.beta2d = None
        self.center = None
        self.beta_shift = None
        self.rebin_beta = None
        self.rebin_alpha = None
        self.rebin_alpha_edges = None
        self.rebin_alpha_mid = None
        self.rebin_beta_edges = None
        self.rebin_beta_mid = None
        self.rebin_alpha2d = None
        self.rebin_beta2d = None
        self.rebin_alpha_ind = None
        self.rebin_beta_ind = None
        self.rebin_pix = None
        self.area2d = None
        self.pixarea = None


    def setup_map(self, nside):
        """Setups the HEALPix map.

        Parameters
        ----------
        nside : int
            HEALPix nside.
        """
        assert hp.isnsideok(nside) == True, "nside given is not ok."
        self.nside = nside


    def setup_polar_cap(self, alpha_min, alpha_max, num_alpha,
                        num_beta, beta_min=0., beta_max=2.*np.pi,
                        center=[0., 0.], beta_shift = 0., rebin_alpha=2, rebin_beta=2):
        """Setups the polar grid.

        Parameters
        ----------
        alpha_min : float
            Minimum alpha.
        alpha_max : float
            Maximum alpha.
        num_alpha : int
            Number of bins along alpha-axis.
        num_beta : int
            Number of bins along beta-axis.
        beta_min : float
            Minimum beta (default=0).
        beta_max : float
            Maximum beta (default=2pi).
        center : list
            Center point of the new polar cap grid.
        beta_shift : float
            Rotation to the polar cap coordinate grid, given in radians within a range
            of 0 and 2pi.
        rebin_alpha : int
            Rebin factor in the alpha axis.
        rebin_beta : int
            Rebin factor in the beta axis.
        """
        assert alpha_min >= 0., "alpha_min must be greater or equal to zero."
        assert alpha_min < alpha_max, "alpha_min must be smaller than alpha_max."
        assert num_alpha > 0, "num_alpha must be greater than zero."
        assert beta_min >= 0., "beta_min must be greater or equal to zero."
        assert beta_min < 2.*np.pi, "beta_min must be smaller than 2pi."
        assert beta_min < beta_max, "beta_min must be smaller than beta_max."
        assert beta_max > 0., "beta_max must be greater than zero."
        assert beta_max <= 2.*np.pi, "beta_max must be smaller of equal to 2pi."
        assert num_beta > 0, "nump must be greater than zero."
        assert len(center) == 2, "center list must have length 2."
        self.alpha_edges = np.linspace(alpha_min, alpha_max, num_alpha+1)
        self.beta_edges = np.linspace(beta_min, beta_max, num_beta+1)
        self.alpha_mid = 0.5*(self.alpha_edges[1:] + self.alpha_edges[:-1])
        self.beta_mid = 0.5*(self.beta_edges[1:] + self.beta_edges[:-1])
        self.dalpha = self.alpha_mid[1] - self.alpha_mid[0]
        self.dbeta = self.beta_mid[1] - self.beta_mid[0]
        self.alpha2d, self.beta2d = np.meshgrid(self.alpha_mid, self.beta_mid)
        self.center = center
        self.beta_shift = beta_shift
        self.rebin_alpha = rebin_alpha
        self.rebin_beta = rebin_beta
        self.rebin_alpha_edges = np.linspace(self.alpha_edges[0], self.alpha_edges[-1], self.rebin_alpha*len(self.alpha_mid) + 1)
        self.rebin_alpha_mid = 0.5*(self.rebin_alpha_edges[1:] + self.rebin_alpha_edges[:-1])
        self.rebin_beta_edges = np.linspace(self.beta_edges[0], self.beta_edges[-1], self.rebin_beta*len(self.beta_mid) + 1)
        self.rebin_beta_mid = 0.5*(self.rebin_beta_edges[1:] + self.rebin_beta_edges[:-1])
        self.rebin_alpha2d, self.rebin_beta2d = np.meshgrid(self.rebin_alpha_mid, self.rebin_beta_mid)
        self.rebin_alpha_ind = np.arange(len(self.rebin_beta2d))
        self.rebin_beta_ind = np.arange(len(self.rebin_beta2d[0]))
        self.rebin_beta_ind, self.rebin_alpha_ind = np.meshgrid(self.rebin_beta_ind, self.rebin_alpha_ind)
        self.rebin_alpha_ind = self.rebin_alpha_ind.flatten()
        self.rebin_beta_ind = self.rebin_beta_ind.flatten()
        if self.beta_shift != 0.:
            phi, theta = coords.usphere_spin(self.rebin_beta2d.flatten(), self.rebin_alpha2d.flatten(), 0., 0., self.beta_shift)
        else:
            phi, theta = self.rebin_beta2d.flatten(), self.rebin_alpha2d.flatten()
        phi, theta = coords.usphere_shift(phi, theta, 0., 0., self.center[0], self.center[1])
        self.rebin_pix = hp.ang2pix(self.nside, theta, phi)


    def _remap(self, f):
        """Remaps 2d grid data f onto polar coordinate grid.

        Parameters
        ----------
        f : array
            HEALPix input map

        Returns
        -------
        f_polar : 2darray
            Remapped 2d data onto polar coordinate grid.
        """
        f_polar_highres = np.zeros(np.shape(self.rebin_alpha2d))
        f_polar_highres[self.rebin_alpha_ind, self.rebin_beta_ind] = f[self.rebin_pix]
        dbeta = self.rebin_beta_edges[1] - self.rebin_beta_edges[0]
        area = np.array([coords.sky_area(0., dbeta, self.rebin_alpha_edges[i], self.rebin_alpha_edges[i+1]) for i in range(0, len(self.rebin_alpha_edges)-1)])
        alpha_bin_weights = area
        alpha_bin_weights_2d, _ = np.meshgrid(alpha_bin_weights, self.rebin_beta_mid)
        f_polar_highres *= alpha_bin_weights_2d
        f_polar = np.sum(f_polar_highres.reshape(len(self.alpha2d), self.rebin_alpha, len(self.rebin_beta2d[0])), axis=1)
        f_polar = np.mean(f_polar.reshape(len(self.alpha2d), len(self.alpha2d[0]), self.rebin_beta), axis=2)
        alpha_bin_weights_2d = np.sum(alpha_bin_weights_2d.reshape(len(self.alpha2d), self.rebin_alpha, len(self.rebin_beta2d[0])), axis=1)
        alpha_bin_weights_2d = np.mean(alpha_bin_weights_2d.reshape(len(self.alpha2d), len(self.alpha2d[0]), self.rebin_beta), axis=2)
        f_polar /= alpha_bin_weights_2d
        return f_polar


    def remap(self, f, w=None, verbose=True):
        """Remaps 2d grid data f onto polar coordinate grid.

        Parameters
        ----------
        f : array
            HEALPix input map
        w : array
            HEALPix weight map.
        verbose : bool
            This does nothing. This is here simply so that no errors occur when
            switching from Monte Carlo weighted remapping to the dense grid remapping.

        Returns
        -------
        f_polar : 2darray
            Remapped 2d data onto polar coordinate grid.
        """
        if w is None:
            f_polar = self._remap(f)
        else:
            f_polar = self._remap(f*w)/self._remap(w)
        return f_polar


    def rotate_polar(self, f_polar, beta_shift):
        """Rotates polar coordinate grid by phi_shift.

        Parameters
        ----------
        f_polar : 2darray
            Polar coordinate gridded data.
        beta_shift : float
            Rotation to be applied, given in radians within a range of 0 and 2pi.

        Returns
        -------
        f_polar_rot : 2darray
            Rotated polar coordinate data.
        """
        assert np.shape(f_polar) == np.shape(self.beta2d), "Shape of f_polar does not match stored polar coordinate grid."
        return coords.rotate_polar(self.beta_edges, f_polar, beta_shift)


    def polar2radial(self, f_polar, sigma=None, w=None, verbose=False):
        """Calculates the radial mean of data provided in a polar coordinate grid
        which originates from a 2D cartesian grid.

        Parameters
        ----------
        f_polar : ndarray
            2D array of a function f in polar coordinates.
        sigma : ndarray
            2D array of the noise for function f in polar coordinates.
        w : ndarray
            2D array containing weights for each pixel in polar grid, ideal for adding
            a binary mask.
        verbose : bool
            If true will print progress, etc.

        Returns
        -------
        f_radial : array
            Radial profile of f.
        sigma_radial : array
            If sigma is provided then the radial errors are outputted.
        """
        if self.area2d is None:
            dbeta = self.beta_edges[1] - self.beta_edges[0]
            area = np.array([coords.sky_area(0., dbeta, self.alpha_edges[i], self.alpha_edges[i+1]) for i in range(0, len(self.alpha_edges)-1)])
            self.area2d = np.array([area for i in range(0, len(self.beta_edges)-1)])
        if self.pixarea is None:
            self.pixarea = hp.nside2pixarea(self.nside)
        assert np.shape(f_polar) == np.shape(self.alpha2d), "Shape of f_polar does not match stored polar-cap coordinate grid."
        if sigma is None:
            f_radial = polar.polar2radial(f_polar, self.area2d, self.pixarea, sigma=sigma, w=w)
            return f_radial
        else:
            assert np.shape(sigma) == np.shape(self.alpha2d), "Shape of sigma does not match stored polar coordinate grid."
            f_radial, sigma_radial = polar.polar2radial(f_polar, self.area2d, self.pixarea, sigma=sigma, w=w)
            return f_radial, sigma_radial


    def clean(self):
        """Cleans by reinitialising the class."""
        self.__init__()
