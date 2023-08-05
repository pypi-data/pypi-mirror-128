import numpy as np
import healpy as hp

from .. import coords
from .. import randoms
from .. import utils


class Cube2Shell:
    """Remaps pixels given on 3D grid to spherical polar grid on a set of HEALPix
    maps.
    """

    def __init__(self):
        """Initialises the class."""
        self.xedges = None
        self.yedges = None
        self.zedges = None
        self.xmid = None
        self.ymid = None
        self.zmid = None
        self.dx = None
        self.dy = None
        self.dz = None
        self.x3d = None
        self.y3d = None
        self.z3d = None
        self.redges = None
        self.nside = None
        self.rmid = None
        self.dr = None
        self.center = None
        self.ind_xs = None
        self.ind_ys = None
        self.ind_zs = None
        self.ind_ws = None


    def setup_cube(self, xmin, xmax, numx, ymin, ymax, numy, zmin, zmax, numz):
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
        self.zedges = np.linspace(zmin, zmax, numz+1)
        self.xmid = 0.5*(self.xedges[1:] + self.xedges[:-1])
        self.ymid = 0.5*(self.yedges[1:] + self.yedges[:-1])
        self.zmid = 0.5*(self.zedges[1:] + self.zedges[:-1])
        self.dx = self.xedges[1] - self.xedges[0]
        self.dy = self.yedges[1] - self.yedges[0]
        self.dz = self.zedges[1] - self.zedges[0]
        self.x3d, self.y3d, self.z3d = np.meshgrid(self.xmid, self.ymid, self.zmid)


    def setup_polar_lin(self, rmin, rmax, numr, nside, center=[0., 0., 0.]):
        """Setups the polar grid.

        Parameters
        ----------
        rmin : float
            Minimum r.
        rmax : float
            Maximum r.
        numr : int
            Number of bins along r-axis.
        nside : int
            Nside for healpix maps for each shell.
        center : list
            Center point of polar coordinate grid.
        """
        assert rmin >= 0., "rmin must be greater or equal to zero."
        assert rmin < rmax, "rmin must be smaller than rmax."
        assert numr > 0, "numr must be greater than zero."
        assert len(center) == 3, "center list must have length 3."
        self.redges = np.linspace(rmin, rmax, numr+1)
        self.rmid = 0.5*(self.redges[1:] + self.redges[:-1])
        self.dr = self.rmid[1] - self.rmid[0]
        self.nside = nside
        self.center = center


    def setup_polar_log(self, rmin, rmax, numr, nside, center=[0., 0., 0.], addzero=True):
        """Setups the polar grid with logarithmic radial bins.

        Parameters
        ----------
        rmin : float
            Minimum r, must be r > 0.
        rmax : float
            Maximum r.
        numr : int
            Number of bins along r-axis.
        nside : int
            Nside for healpix maps for each shell.
        center : list
            Center point of polar coordinate grid.
        addzero : bool
            Adds r=0 to the radial edges.
        """
        assert rmin > 0., "rmin must be greater than zero."
        assert rmin < rmax, "rmin must be smaller than rmax."
        assert numr > 0, "numr must be greater than zero."
        assert len(center) == 3, "center list must have length 3."
        if addzero == True:
            self.redges = np.zeros(numr+1)
            self.redges[1:] = np.logspace(np.log10(rmin), np.log10(rmax), numr)
        else:
            self.redges = np.logspace(np.log10(rmin), np.log10(rmax), numr+1)
        self.rmid = 0.5*(self.redges[1:] + self.redges[:-1])
        self.dr = self.redges[1:] - self.redges[:-1]
        self.nside = nside
        self.center = center


    def get_weights(self, mc_size=100, verbose=True):
        """Calculates Monte Carlo pixel weights for remapping from cartesian grid
        to spherical polar coordinate grid on healpix map.

        Parameters
        ----------
        mc_size : int
            Size of the Monte Carlo random points for calculating weights from Monte
            Carlo integration.
        verbose : bool
            If true will output a progress bar.
        """
        ind_xs = []
        ind_ys = []
        ind_zs = []
        ind_ws = []
        for i in range(0, len(self.rmid)):
            _ind_xs = []
            _ind_ys = []
            _ind_zs = []
            _ind_ws = []
            for j in range(0, hp.nside2npix(self.nside)):
                pix = j
                rmin, rmax = self.redges[i], self.redges[i+1]
                phi_rand, theta_rand = randoms.randoms_healpix_pixel(mc_size, pix, self.nside)
                r_rand = randoms.randoms_sphere_r(mc_size, r_min=rmin, r_max=rmax)
                xrand, yrand, zrand = coords.sphere2cart(r_rand, phi_rand, theta_rand, center=self.center)
                H, _ = np.histogramdd((xrand, yrand, zrand), bins=[len(self.xedges)-1, len(self.yedges)-1, len(self.zedges)-1],
                                      range=[[self.xedges[0], self.xedges[-1]], [self.yedges[0], self.yedges[-1]], [self.zedges[0], self.zedges[-1]]])
                condition = np.where(H != 0.)
                ind_x = condition[1]
                ind_y = condition[0]
                ind_z = condition[2]
                ind_w = H[condition]/float(mc_size)
                _ind_xs.append(ind_x)
                _ind_ys.append(ind_y)
                _ind_zs.append(ind_z)
                _ind_ws.append(ind_w)
            ind_xs.append(np.array(_ind_xs, dtype=object))
            ind_ys.append(np.array(_ind_ys, dtype=object))
            ind_zs.append(np.array(_ind_zs, dtype=object))
            ind_ws.append(np.array(_ind_ws, dtype=object))
            if verbose == True:
                utils.progress_bar(i, len(self.rmid), explanation='Calculating weights')
        self.ind_xs = np.array(ind_xs, dtype=object)
        self.ind_ys = np.array(ind_ys, dtype=object)
        self.ind_zs = np.array(ind_zs, dtype=object)
        self.ind_ws = np.array(ind_ws, dtype=object)


    def remap(self, f, w=None, verbose=True):
        """Remaps 3d grid data f onto spherical polar coordinate grid.

        Parameters
        ----------
        f : 3darray
            3d pixel data.
        w : 3darray
            Weights.
        verbose : bool
            If true will output a progress bar.

        Returns
        -------
        f_sphere : 2darray
            Remapped 3d grid data on to spherical polar coordinates (in healpix shells).
        """
        f_sphere = np.zeros((len(self.rmid), hp.nside2npix(self.nside)))
        for i in range(0, len(self.rmid)):
            for j in range(0, hp.nside2npix(self.nside)):
                pix = j
                if w is None:
                    if np.sum(self.ind_ws[i, j]) != 0.:
                        f_sphere[i, j] = np.sum(self.ind_ws[i, j]*f[self.ind_xs[i, j], self.ind_ys[i, j], self.ind_zs[i, j]])
                        f_sphere[i, j] /= np.sum(self.ind_ws[i, j])
                    else:
                        f_sphere[i, j] = hp.UNSEEN
                else:
                    if np.sum(self.ind_ws[i, j]) != 0.:
                        f_sphere[i, j] = np.sum(self.ind_ws[i, j]*w[self.ind_xs[i, j], self.ind_ys[i, j], self.ind_zs[i, j]]*f[self.ind_xs[i, j], self.ind_ys[i, j], self.ind_zs[i, j]])
                        f_sphere[i, j] /= np.sum(self.ind_ws[i, j]*w[self.ind_xs[i, j], self.ind_ys[i, j], self.ind_zs[i, j]])
                    else:
                        f_sphere[i, j] = hp.UNSEEN
            if verbose == True:
                utils.progress_bar(i, len(self.rmid), explanation='Remapping')
        return f_sphere


    def clean(self):
        """Cleans by reinitialising the class."""
        self.__init__()
