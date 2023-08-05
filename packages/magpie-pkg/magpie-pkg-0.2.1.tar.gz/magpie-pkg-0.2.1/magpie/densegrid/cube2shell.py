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
        self.rebin_shell = None
        self.rebin_r = None
        self.centers = None
        self.rebin_redges = None
        self.rebin_rmid = None

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


    def setup_polar(self, rmin, rmax, numr, nside, center=[0., 0., 0.], rebin_shell=2,
                    rebin_r=2, periodicx=[0, 0], periodicy=[0, 0], periodicz=[0, 0]):
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
        rebin_shell : int
            Integer factor (a power of 2) for regriding the healpix shells to a
            higher nside than desired. This is then downgraded to the desired nside.
        rebin_r : int
            Integer factor for regridding the r axis by a factor rebin_r. This is
            then rebinned to the desired grid.
        """
        assert rmin >= 0., "rmin must be greater or equal to zero."
        assert rmin < rmax, "rmin must be smaller than rmax."
        assert numr > 0, "numr must be greater than zero."
        assert len(center) == 3, "center list must have length 3."
        assert rebin_shell >= 1, "rebin_shell must be greater or equal to 1."
        assert hp.isnsideok(nside) == True, "Incompatible nside."
        assert hp.isnsideok(nside*rebin_shell) == True, "Incompatible shell_rebin must be power of 2."
        assert rebin_r >= 1, "rebin_r must be greater or equal to 1."
        self.redges = np.linspace(rmin, rmax, numr+1)
        self.rmid = 0.5*(self.redges[1:] + self.redges[:-1])
        self.dr = self.rmid[1] - self.rmid[0]
        self.nside = nside
        self.center = center
        self.rebin_shell = rebin_shell
        self.rebin_r = rebin_r
        centers = []
        for i in range(periodicx[0], periodicx[1]+1):
            for j in range(periodicy[0], periodicy[1]+1):
                for k in range(periodicz[0], periodicz[1]+1):
                    centers.append([center[0] + i*(self.xedges[-1]-self.xedges[0]),
                                    center[1] + j*(self.yedges[-1]-self.yedges[0]),
                                    center[2] + k*(self.zedges[-1]-self.zedges[0])])
        self.centers = centers
        self.rebin_redges = np.linspace(self.redges[0], self.redges[-1], self.rebin_r*len(self.rmid) + 1)
        self.rebin_rmid = 0.5*(self.rebin_redges[1:] + self.rebin_redges[:-1])


    def remap(self, f, verbose=True):
        """Remaps 3d grid data f onto spherical polar coordinate grid.

        Parameters
        ----------
        f : 3darray
            3d pixel data.
        verbose : bool
            If true will output a progress bar.

        Returns
        -------
        f_sphere : 2darray
            Remapped 3d grid data on to spherical polar coordinates (in healpix shells).
        """
        f_sphere = np.zeros((len(self.rebin_rmid), hp.nside2npix(self.nside)))
        for i in range(0, len(self.rebin_rmid)):
            f_shell_highres = np.zeros(hp.nside2npix(self.nside*self.rebin_shell))
            pix = np.arange(hp.nside2npix(self.nside*self.rebin_shell))
            theta, phi = hp.pix2ang(self.nside*self.rebin_shell, pix)
            r = np.ones(len(phi))*self.rebin_rmid[i]
            for j in range(0, len(self.centers)):
                x, y, z = coords.sphere2cart(r, phi, theta, center=self.centers[j])
                x -= self.xedges[0]
                y -= self.yedges[0]
                z -= self.zedges[0]
                xind = x / self.dx
                yind = y / self.dy
                zind = z / self.dz
                xind = np.floor(xind).astype(int)
                yind = np.floor(yind).astype(int)
                zind = np.floor(zind).astype(int)
                condition = np.where((xind >= 0) & (xind < len(self.xmid)) & (yind >= 0) & (yind < len(self.ymid)) & (zind >= 0) & (zind < len(self.zmid)))[0]
                f_shell_highres[pix[condition]] = f[xind[condition], yind[condition], zind[condition]]
            f_sphere[i] = hp.ud_grade(f_shell_highres, self.nside)
            if verbose == True:
                utils.progress_bar(i, len(self.rebin_rmid), explanation='Remapping')
        if verbose == True:
            print('Downgrading to desired spherical polar coordinate grid...')
        rbin_weights = self.rebin_redges[1:]**3 - self.rebin_redges[:-1]**3
        f_sphere = np.array([f_sphere[i]*rbin_weights[i] for i in range(0, len(f_sphere))])
        rbin_weights_sum = np.sum(rbin_weights.reshape(len(self.rmid), self.rebin_r), axis=1)
        f_sphere = np.sum(f_sphere.reshape(len(self.rmid), self.rebin_r, hp.nside2npix(self.nside)), axis=1)
        f_sphere = np.array([f_sphere[i]/rbin_weights_sum[i] for i in range(0, len(f_sphere))])
        if verbose == True:
            print('Done!')
        return f_sphere


    def clean(self):
        """Cleans by reinitialising the class."""
        self.__init__()
