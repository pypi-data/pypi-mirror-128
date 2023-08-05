import numpy as np

from .. import coords
from .. import polar
from .. import randoms
from .. import utils


class Box2Ring:
    """Remaps pixels given on 2D grid to polar grid."""


    def __init__(self):
        """Initialises the class."""
        self.xedges = None
        self.yedges = None
        self.xmid = None
        self.ymid = None
        self.dx = None
        self.dy = None
        self.x2d = None
        self.y2d = None
        self.redges = None
        self.pedges = None
        self.rmid = None
        self.pmid = None
        self.dr = None
        self.dp = None
        self.r2d = None
        self.p2d = None
        self.center = None
        self.phi_shift = None
        self.rebin_p = None
        self.rebin_r = None
        self.rebin_redges = None
        self.rebin_rmid = None
        self.rebin_pedges = None
        self.rebin_pmid = None
        self.rebin_r2d = None
        self.rebin_p2d = None
        self.area2d = None
        self.pixarea = None
        self.mask_in_bound = None


    def setup_box(self, xmin, xmax, numx, ymin, ymax, numy):
        """Setups the box grid.

        Parameters
        ----------
        xmin : float
            Minimum x.
        xmax : float
            Maximum x.
        numx : int
            Number of bins along x-axis.
        ymin : float
            Minimum y.
        ymax : float
            Maximum y.
        numy : int
            Number of bins along y-axis.
        """
        assert numx > 0, "numx must be greater than zero."
        assert numy > 0, "numy must be greater than zero."
        self.xedges = np.linspace(xmin, xmax, numx+1)
        self.yedges = np.linspace(ymin, ymax, numy+1)
        self.xmid = 0.5*(self.xedges[1:] + self.xedges[:-1])
        self.ymid = 0.5*(self.yedges[1:] + self.yedges[:-1])
        self.dx = self.xedges[1] - self.xedges[0]
        self.dy = self.yedges[1] - self.yedges[0]
        self.x2d, self.y2d = np.meshgrid(self.xmid, self.ymid)


    def setup_polar(self, rmin, rmax, numr, nump, pmin=0., pmax=2.*np.pi, center=[0., 0.], rebin_r=2, rebin_p=2, phi_shift=0.):
        """Setups the polar grid.

        Parameters
        ----------
        rmin : float
            Minimum r.
        rmax : float
            Maximum r.
        numr : int
            Number of bins along r-axis.
        nump : int
            Number of bins along phi-axis.
        pmin : float
            Minimum phi (default=0).
        pmax : float
            Maximum phi (default=2pi).
        center : list
            Center point of polar coordinate grid.
        phi_shift : float
            Rotation to the polar coordinate grid, given in radians within a range
            of 0 and 2pi.
        rebin_r : int
            Rebin factor in the r-axis.
        rebin_p : int
            Rebin factor in the phi-axis.
        """
        assert rmin >= 0., "rmin must be greater or equal to zero."
        assert rmin < rmax, "rmin must be smaller than rmax."
        assert numr > 0, "numr must be greater than zero."
        assert pmin >= 0., "pmin must be greater or equal to zero."
        assert pmin < 2.*np.pi, "pmin must be smaller than 2pi."
        assert pmin < pmax, "pmin must be smaller than pmax."
        assert pmax > 0., "pmax must be greater than zero."
        assert pmax <= 2.*np.pi, "pmax must be smaller of equal to 2pi."
        assert nump > 0, "nump must be greater than zero."
        assert len(center) == 2, "center list must have length 2."
        self.redges = np.linspace(rmin, rmax, numr+1)
        self.pedges = np.linspace(pmin, pmax, nump+1)
        self.rmid = 0.5*(self.redges[1:] + self.redges[:-1])
        self.pmid = 0.5*(self.pedges[1:] + self.pedges[:-1])
        self.dr = self.rmid[1] - self.rmid[0]
        self.dp = self.pmid[1] - self.pmid[0]
        self.r2d, self.p2d = np.meshgrid(self.rmid, self.pmid)
        self.center = center
        self.phi_shift = phi_shift
        self.rebin_r = rebin_r
        self.rebin_p = rebin_p
        self.rebin_redges = np.linspace(self.redges[0], self.redges[-1], self.rebin_r*len(self.rmid) + 1)
        self.rebin_rmid = 0.5*(self.rebin_redges[1:] + self.rebin_redges[:-1])
        self.rebin_pedges = np.linspace(self.pedges[0], self.pedges[-1], self.rebin_p*len(self.pmid) + 1)
        self.rebin_pmid = 0.5*(self.rebin_pedges[1:] + self.rebin_pedges[:-1])
        self.rebin_r2d, self.rebin_p2d = np.meshgrid(self.rebin_rmid, self.rebin_pmid)
        if self.phi_shift != 0.:
            self.rebin_p2d += self.phi_shift
            condition = np.where(self.rebin_p2d > 2.*np.pi)
            self.rebin_p2d[condition] -= 2.*np.pi
            condition = np.where(self.rebin_p2d < 0.)
            self.rebin_p2d[condition] += 2.*np.pi

    def _remap(self, f):
        """Remaps 2d grid data f onto polar coordinate grid.

        Parameters
        ----------
        f : 2darray
            2d pixel data.
        w : 2darray
            2d pixel weights.

        Returns
        -------
        f_polar : 2darray
            Remapped 2d data onto polar coordinate grid.
        """
        f_polar_highres = np.zeros(np.shape(self.rebin_r2d))
        x, y = coords.polar2cart(self.rebin_r2d, self.rebin_p2d, center=self.center)
        x -= self.xedges[0]
        y -= self.yedges[0]
        xind = x / self.dx
        yind = y / self.dy
        xind = np.floor(xind).astype(int)
        yind = np.floor(yind).astype(int)
        condition = np.where((xind >= 0) & (xind < len(self.xmid)) & (yind >= 0) & (yind < len(self.ymid)))
        f_polar_highres[condition] = f[yind[condition], xind[condition]]
        rbin_weights = self.rebin_redges[1:]**2 - self.rebin_redges[:-1]**2
        rbin_weights_2d, _ = np.meshgrid(rbin_weights, self.rebin_pmid)
        f_polar_highres *= rbin_weights_2d
        f_polar = np.sum(f_polar_highres.reshape(len(self.r2d), self.rebin_r, len(self.rebin_p2d[0])), axis=1)
        f_polar = np.mean(f_polar.reshape(len(self.r2d), len(self.r2d[0]), self.rebin_p), axis=2)
        rbin_weights_2d = np.sum(rbin_weights_2d.reshape(len(self.r2d), self.rebin_r, len(self.rebin_p2d[0])), axis=1)
        rbin_weights_2d = np.mean(rbin_weights_2d.reshape(len(self.r2d), len(self.r2d[0]), self.rebin_p), axis=2)
        f_polar /= rbin_weights_2d
        return f_polar


    def remap(self, f, w=None, verbose=True):
        """Remaps 2d grid data f onto polar coordinate grid.

        Parameters
        ----------
        f : 2darray
            2d pixel data.
        w : 2darray
            2d pixel weights.
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


    def get_mask_in_bound(self, verbose=True):
        """Returns a mask showing whether the polar grid remains inside the boundaries
        of the initial cartesian grid.

        Parameters
        ----------
        verbose : bool
            If true will print progress, etc.
        """
        assert self.x2d is not None, "Cartesian grid is not defined."
        assert self.r2d is not None, "Polar grid is not defined."
        if verbose == True:
            print("Construct mask_in_bound...")
        mask = np.ones(np.shape(self.x2d))
        mask_in_bound = self.remap(mask, verbose=verbose)
        condition = np.where(np.isfinite(mask_in_bound) == False)
        mask_in_bound[condition] = 0.
        self.mask_in_bound = mask_in_bound


    def rotate_polar(self, f_polar, phi_shift):
        """Rotates polar coordinate grid by phi_shift.

        Parameters
        ----------
        f_polar : 2darray
            Polar coordinate gridded data.
        phi_shift : float
            Rotation to be applied, given in radians within a range of 0 and 2pi.

        Returns
        -------
        f_polar_rot : 2darray
            Rotated polar coordinate data.
        """
        assert np.shape(f_polar) == np.shape(self.p2d), "Shape of f_polar does not match stored polar coordinate grid."
        return coords.rotate_polar(self.pedges, f_polar, phi_shift)


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
            self.area2d = polar.get_polar_area2d(self.redges, self.pedges)
        if self.pixarea is None:
            self.pixarea = polar.get_pixarea(self.xedges, self.yedges)
        assert np.shape(f_polar) == np.shape(self.p2d), "Shape of f_polar does not match stored polar coordinate grid."
        if self.mask_in_bound is None:
            self.get_mask_in_bound(verbose=verbose)
        if self.mask_in_bound.all() != 1.:
            condition = np.where(self.mask_in_bound != 1.)
            f_polar = np.copy(f_polar)
            f_polar[condition] = 0.
            if sigma is not None:
                sigma = np.copy(sigma)
                sigma[condition] = 0.
            if w is not None:
                w *= self.mask_in_bound
            else:
                w = self.mask_in_bound
        if sigma is None:
            f_radial = polar.polar2radial(f_polar, self.area2d, self.pixarea, sigma=sigma, w=w)
            return f_radial
        else:
            assert np.shape(sigma) == np.shape(self.p2d), "Shape of sigma does not match stored polar coordinate grid."
            f_radial, sigma_radial = polar.polar2radial(f_polar, self.area2d, self.pixarea, sigma=sigma, w=w)
            return f_radial, sigma_radial


    def clean(self):
        """Cleans by reinitialising the class."""
        self.__init__()
