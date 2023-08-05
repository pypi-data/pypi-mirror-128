import numpy as np
import healpy as hp

from .. import coords
from .. import polar
from .. import randoms
from .. import utils


class Heal2Ring:
    """Remaps pixels given a HEALPix map to a polar cap grid."""

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
        self.ind_pixs = None
        self.ind_ws = None
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


    def setup_polar_cap(self, alpha_min, alpha_max, num_alpha, num_beta, beta_min=0., beta_max=2.*np.pi,
                        center=[0., 0.], beta_shift=0.):
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
        """
        assert alpha_min >= 0., "alpha_min must be greater or equal to zero."
        assert alpha_min < alpha_max, "alpha_min must be smaller than alpha_max."
        assert num_alpha > 0, "num_alpha must be greater than zero."
        assert beta_min >= 0., "beta_min must be greater or equal to zero."
        assert beta_min < 2.*np.pi, "beta_min must be smaller than 2pi."
        assert beta_min < beta_max, "beta_min must be smaller than beta_max."
        assert beta_max > 0., "beta_max must be greater than zero."
        assert beta_max <= 2.*np.pi, "beta_max must be smaller of equal to 2pi."
        assert num_beta > 0, "num_beta must be greater than zero."
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


    def get_weights(self, mc_size=10000, verbose=True):
        """Calculates Monte Carlo pixel weights for remapping from cartesian grid
        to polar coordinate grid.

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
        for i in range(0, len(self.alpha2d)):
            _ind_pixs = []
            _ind_ws = []
            for j in range(0, len(self.alpha2d[0])):
                alpha_min, alpha_max = self.alpha_edges[j], self.alpha_edges[j+1]
                beta_min, beta_max = self.beta_edges[i], self.beta_edges[i+1]
                beta_rand, alpha_rand = randoms.randoms_sky(mc_size, phi_min=beta_min, phi_max=beta_max,
                                                            theta_min=alpha_min, theta_max=alpha_max)
                if self.beta_shift != 0.:
                    beta_rand, alpha_rand = coords.usphere_spin(beta_rand, alpha_rand, 0., 0., self.beta_shift)
                phi_rand, theta_rand = coords.usphere_shift(beta_rand, alpha_rand, 0., 0., self.center[0], self.center[1])
                pix_rand = hp.ang2pix(self.nside, theta_rand, phi_rand)
                pix_uniq, pix_counts = np.unique(pix_rand, return_counts=True)
                ind_pix = pix_uniq
                ind_w = (pix_counts.astype('float'))/float(mc_size)
                _ind_pixs.append(ind_pix)
                _ind_ws.append(ind_w)
            ind_pixs.append(np.array(_ind_pixs, dtype=object))
            ind_ws.append(np.array(_ind_ws, dtype=object))
            if verbose == True:
                utils.progress_bar(i, len(self.alpha2d), explanation='Calculating weights')
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
        f_polar = np.zeros(np.shape(self.beta2d))
        for i in range(0, len(self.alpha2d)):
            for j in range(0, len(self.alpha2d[0])):
                if w is None:
                    if np.sum(self.ind_ws[i, j]) != 0.:
                        f_polar[i, j] = np.sum(self.ind_ws[i, j]*f[self.ind_pixs[i, j]])
                        f_polar[i, j] /= np.sum(self.ind_ws[i, j])
                    else:
                        f_polar[i, j] = np.nan
                else:
                    if np.sum(self.ind_ws[i, j]) != 0.:
                        f_polar[i, j] = np.sum(self.ind_ws[i, j]*w[self.ind_pixs[i, j]]*f[self.ind_pixs[i, j]])
                        f_polar[i, j] /= np.sum(self.ind_ws[i, j]*w[self.ind_pixs[i, j]])
                    else:
                        f_polar[i, j] = np.nan
            if verbose == True:
                utils.progress_bar(i, len(self.alpha2d), explanation='Remapping')
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
