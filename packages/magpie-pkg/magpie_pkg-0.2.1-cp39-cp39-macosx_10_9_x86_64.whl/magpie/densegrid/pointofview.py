import numpy as np

from .. import coords


class PointOfView:

    """Transforms 3 dimensional coordinates to a 2D perspective."""

    def __init__(self):
        """Initialises the class."""
        self.camera    = None
        self.point     = None
        self.display   = None
        self.phi_point_towards   = None
        self.theta_point_towards = None
        self.spin      = None


    def setup(self, camera, point, display, spin=0.):
        """Setup the perpective view.

        Parameters
        ----------
        camera : list
            3D coordinates of the perspective.
        point : list
            3D coordinates of the direction to point.
        display : float
            Distance to display plane.
        spin : float, optional
            rotate the perspective around the central point defined by point.
        """
        self.camera  = camera
        self.point   = point
        self.display = display
        _r, _phi, _theta = coords.cart2sphere(self.point[0], self.point[1], self.point[2], center=self.camera)
        self.phi_point_towards = _phi
        self.theta_point_towards = _theta
        self.spin = spin


    def transform(self, x, y, z):
        """Transforming from 3D coordinates to the perspective view.

        Parameters
        ----------
        x : array
            X-axis coordinates.
        y : array
            Y-axis coordinates.
        z : array
            Z-axis coordinates

        Returns
        -------
        bx : array
            Perspective x-coordinate.
        by : array
            Perspective y-coordinate.
        dist : array
            Distance of coordinates from the camera.
        """
        r, phi, theta = coords.cart2sphere(x, y, z, center=self.camera)
        if self.theta_point_towards != np.pi/2.:
            phi, theta = coords.usphere_rotate(phi, theta, self.phi_point_towards, np.pi/2., phi_start=self.phi_point_towards, theta_start=self.theta_point_towards)
        phi = coords.usphere_phi_shift(phi, -self.phi_point_towards)
        if self.spin != 0.:
            phi, theta = coords.usphere_spin(phi, theta, 0., np.pi/2., self.spin)
        dx, dy, dz = coords.sphere2cart(r, phi, theta)
        f = self.display/dx
        condition = np.where(f >= 1.)[0]
        bx = dy*f
        by = dz*f
        dist = np.sqrt(dx**2. + dy**2. + dz**2.)
        return bx, by, dist


    def reverse(self, bx, by, dist):
        """Transforming from the perspective view coordinates to 3D coordinates.

        Parameters
        ----------
        bx : array
            Perspective x-coordinate.
        by : array
            Perspective y-coordinate.
        dist : array
            Distance of coordinates from the camera.

        Returns
        -------
        x : array
            X-axis coordinates.
        y : array
            Y-axis coordinates.
        z : array
            Z-axis coordinates
        """
        dx = dist / np.sqrt(1. + (1./(self.display**2.))*(bx**2. + by**2.))
        f = self.display/dx
        dy = bx / f
        dz = by / f
        r, phi, theta = coords.cart2sphere(dx, dy, dz)
        if self.spin != 0.:
            phi, theta = coords.usphere_spin(phi, theta, 0., np.pi/2., -self.spin)
        phi = coords.usphere_phi_shift(phi, self.phi_point_towards)
        if self.theta_point_towards != np.pi/2.:
            phi, theta = coords.usphere_rotate(phi, theta, self.phi_point_towards, self.theta_point_towards, phi_start=self.phi_point_towards, theta_start=np.pi/2.)
        x, y, z = coords.sphere2cart(r, phi, theta, center=self.camera)
        return x, y, z


    def clean(self):
        """Reinitialises the class."""
        self.__init__()
