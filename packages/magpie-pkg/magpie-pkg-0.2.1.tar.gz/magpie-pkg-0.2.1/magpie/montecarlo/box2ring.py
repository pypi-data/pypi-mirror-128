import numpy as np

from .. import coords
from .. import polar
from .. import randoms
from .. import utils


class Box2Ring:
    """Remaps pixels given on 2D grid to polar grid.

    Note
    ----

    p is used as a shorthand for phi in the naming of variables.

    Example
    -------

    import numpy as np
    import magpie

    # Initialise magpie Box2Ring class
    b2r = magpie.mc.Box2Ring()

    # Setup the box grid
    b2r.setup_box(-20., 20., 100, -20., 20., 100)

    # Create an 'interesting' function for remapping
    # I'm using a Bessel function of order 5 multiplied by a sine wave
    f = np.zeros(np.shape(b2r.x2d))
    r, phi = magpie.coords.cart2polar(b2r.x2d, b2r.y2d)
    f = special.jv(5, r)*np.sin(phi*5)

    # Construct polar grid
    b2r.setup_polar_lin(0., 20., 50, 150, center=[0., 0.])
    # Calculate monte carlo weights for remapping
    b2r.get_weights()
    # The weights for a particular remapping can be stored.

    # Now, let's remap the function from a linear cartesian grid to polar coordinates
    f_polar = b2r.remap(f)
    """

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
        self.ind_xs = None
        self.ind_ys = None
        self.ind_ws = None
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


    def setup_polar_lin(self, rmin, rmax, numr, nump, pmin=0., pmax=2.*np.pi,
                        center=[0., 0.], phi_shift=0.):
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


    def setup_polar_log(self, rmin, rmax, numr, nump, pmin=0., pmax=2.*np.pi,
                        center=[0., 0.], phi_shift=0., addzero=True):
        """Setups the polar grid with logarithmic radial bins.

        Parameters
        ----------
        rmin : float
            Minimum r, must be r > 0.
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
        addzero : bool
            Adds r=0 to the radial edges.
        """
        assert rmin > 0., "rmin must be greater than zero."
        assert rmin < rmax, "rmin must be smaller than rmax."
        assert numr > 0, "numr must be greater than zero."
        assert pmin >= 0., "pmin must be greater or equal to zero."
        assert pmin < 2.*np.pi, "pmin must be smaller than 2pi."
        assert pmin < pmax, "pmin must be smaller than pmax."
        assert pmax > 0., "pmax must be greater than zero."
        assert pmax <= 2.*np.pi, "pmax must be smaller of equal to 2pi."
        assert nump > 0, "nump must be greater than zero."
        assert len(center) == 2, "center list must have length 2."
        if addzero == True:
            self.redges = np.zeros(numr+1)
            self.redges[1:] = np.logspace(np.log10(rmin), np.log10(rmax), numr)
        else:
            self.redges = np.logspace(np.log10(rmin), np.log10(rmax), numr+1)
        self.pedges = np.linspace(pmin, pmax, nump+1)
        self.rmid = 0.5*(self.redges[1:] + self.redges[:-1])
        self.pmid = 0.5*(self.pedges[1:] + self.pedges[:-1])
        self.dr = self.redges[1:] - self.redges[:-1]
        self.dp = self.pmid[1] - self.pmid[0]
        self.r2d, self.p2d = np.meshgrid(self.rmid, self.pmid)
        self.center = center
        self.phi_shift = phi_shift


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
        ind_xs = []
        ind_ys = []
        ind_ws = []
        for i in range(0, len(self.r2d)):
            _ind_xs = []
            _ind_ys = []
            _ind_ws = []
            for j in range(0, len(self.r2d[0])):
                rmin, rmax = self.redges[j], self.redges[j+1]
                pmin, pmax = self.pedges[i], self.pedges[i+1]
                rrand, prand = randoms.randoms_polar(mc_size, rmin, rmax, pmin, pmax)
                if self.phi_shift != 0.:
                    prand += self.phi_shift
                    condition = np.where(prand > 2.*np.pi)
                    prand[condition] -= 2.*np.pi
                    condition = np.where(prand < 0.)
                    prand[condition] += 2.*np.pi
                xrand, yrand = coords.polar2cart(rrand, prand, center=self.center)
                H, _ = np.histogramdd((xrand, yrand), bins=[len(self.xedges)-1, len(self.yedges)-1],
                                      range=[[self.xedges[0], self.xedges[-1]],[self.yedges[0], self.yedges[-1]]])
                condition = np.where(H != 0.)
                ind_x = condition[1]
                ind_y = condition[0]
                ind_w = H[condition]/float(mc_size)
                _ind_xs.append(ind_x)
                _ind_ys.append(ind_y)
                _ind_ws.append(ind_w)
            ind_xs.append(np.array(_ind_xs, dtype=object))
            ind_ys.append(np.array(_ind_ys, dtype=object))
            ind_ws.append(np.array(_ind_ws, dtype=object))
            if verbose == True:
                utils.progress_bar(i, len(self.r2d), explanation='Calculating weights')
        self.ind_xs = np.array(ind_xs, dtype=object)
        self.ind_ys = np.array(ind_ys, dtype=object)
        self.ind_ws = np.array(ind_ws, dtype=object)


    def remap(self, f, w=None, verbose=True):
        """Remaps 2d grid data f onto polar coordinate grid.

        Parameters
        ----------
        f : 2darray
            2d pixel data.
        w : 2darray
            Weights.
        verbose : bool
            If true will output a progress bar.

        Returns
        -------
        f_polar : 2darray
            Remapped 2d data onto polar coordinate grid.
        """
        assert np.shape(f) == np.shape(self.x2d), "Shape of f does not match stored cartesian grid."
        if w is not None:
            assert np.shape(w) == np.shape(self.x2d), "Shape of w does not match stored cartesian grid."
        f_polar = np.zeros(np.shape(self.r2d))
        for i in range(0, len(self.r2d)):
            for j in range(0, len(self.r2d[0])):
                if w is None:
                    if np.sum(self.ind_ws[i, j]) != 0.:
                        f_polar[i, j] = np.sum(self.ind_ws[i, j]*f[self.ind_xs[i, j], self.ind_ys[i, j]])
                        f_polar[i, j] /= np.sum(self.ind_ws[i, j])
                    else:
                        f_polar[i, j] = np.nan
                else:
                    if np.sum(self.ind_ws[i, j]) != 0.:
                        f_polar[i, j] = np.sum(self.ind_ws[i, j]*w[self.ind_xs[i, j], self.ind_ys[i, j]]*f[self.ind_xs[i, j], self.ind_ys[i, j]])
                        f_polar[i, j] /= np.sum(self.ind_ws[i, j]*w[self.ind_xs[i, j], self.ind_ys[i, j]])
                    else:
                        f_polar[i, j] = np.nan
            if verbose == True:
                utils.progress_bar(i, len(self.r2d), explanation='Remapping')
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
