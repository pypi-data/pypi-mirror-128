import numpy as np
import matplotlib.pylab as plt
import scipy.interpolate as interpolate

from . import shapes as plot_shapes
from .. import coords
from .. import shapes


class PlotOrtho:


    def __init__(self, heal2ortho):
        """

        Parameters
        ----------
        heal2ortho : class
            For transformation.
        """
        self.heal2ortho = heal2ortho


    def imshow(self, dmap, cmap=plt.cm.viridis, ax=None, returncb=False, **kwargs):
        """

        Parameters
        ----------
        dmap : 2darray
            Data map given in orthographic projection.
        cmap : class, optional
            Colormap.
        ax : class, optional
            Axis to plot on.
        returncb : bool, optional
            Return imshow for colorbar plots.
        """
        if ax is None:
            cb = plt.imshow(dmap, origin='lower', extent=[self.heal2ortho.xedges[0], self.heal2ortho.xedges[-1],
                           self.heal2ortho.yedges[0], self.heal2ortho.yedges[-1]], cmap=cmap, **kwargs)
        else:
            cb = ax.imshow(dmap, origin='lower', extent=[self.heal2ortho.xedges[0], self.heal2ortho.xedges[-1],
                           self.heal2ortho.yedges[0], self.heal2ortho.yedges[-1]], cmap=cmap, **kwargs)
        if returncb == True:
            return cb


    def plot_grid(self, dtheta=15., dphi=None, zeropoint=[0., np.pi/2.],
                  shift=[1.5, 2.], ax=None, color='k', linestyle='--', **kwargs):
        """Plots labels on the orthographic grid.

        Parameters
        ----------
        dtheta : float, optional
            Separation in the grid.
        dphi : float, optional
            To specify different grid spacing in phi.
        zeropoint : list, optional
            Axis zero-point.
        shift : list, optional
            Shift in degrees to place on the coordinates.
        ax : class, optional
            Axis to plot on.
        color : str, optional
            Color of the grid lines.
        linestyle : str, optional
            Linestyle of the grid lines.
        """
        if dphi is None:
            dphi = dtheta
        nlines = int(360/dphi)
        phi_grid = np.linspace(0., 2.*np.pi, nlines + 1)[:-1]
        nlines = int(180/dtheta)
        theta_grid = np.linspace(0., np.pi, nlines + 1)[:-1]

        for ii in range(0, len(phi_grid)):
            points = 100
            phi = np.ones(points)*phi_grid[ii]
            theta = np.linspace(0., np.pi, points)
            x, y = self.heal2ortho.transform(phi, theta)
            if ax is None:
                plt.plot(x, y, color=color, linestyle=linestyle, **kwargs)
            else:
                ax.plot(x, y, color=color, linestyle=linestyle, **kwargs)

        for ii in range(0, len(theta_grid)):
            points = 100
            theta = np.ones(points)*theta_grid[ii]
            phi = np.linspace(0., 2.*np.pi, points)
            x, y = self.heal2ortho.transform(phi, theta)
            if ax is None:
                plt.plot(x, y, color=color, linestyle=linestyle, **kwargs)
            else:
                ax.plot(x, y, color=color, linestyle=linestyle, **kwargs)


    def plot_labels(self, dtheta=15., dphi=None, decimals=0, lonlat=False, zeropoint=[0., np.pi/2.],
                    shift=[0., 0.], ax=None, onsphere=False, userotation=False, ha='left', va='top',
                    interpaxis=100, **kwargs):
        """Plots labels on the orthographic grid.

        Parameters
        ----------
        heal2ortho : class
            For transformation.
        dtheta : float, optional
            Separation in the grid.
        dphi : float, optional
            To specify different grid spacing in phi.
        decimals : int, optional
            Number of decimals to place in labels.
        lonlat : bool, optional
            Determines whether to plot coordinates in longitude and latitude.
        zeropoint : list, optional
            Axis zero-point.
        shift : list, optional
            Shift in degrees to place on the coordinates.
        ax : class, optional
            Axis to plot on.
        onsphere : bool, optional
            Plots axis on the sphere rather than on the edges.
        userotation : bool, optional
            Rotates labels automatically, if onsphere is True.
        ha : str, optional
            Horizontal alignment, if onsphere is True.
        va : str, optional
            Vertical alignment, if onsphere is True.
        interpaxis : int, optional
            Used to interpolate grid points on the x and y axis, only used if onsphere is False.
        """
        if dphi is None:
            dphi = dtheta
        nlines = int(360/dphi)
        phi_grid = np.linspace(0., 2.*np.pi, nlines + 1)[:-1]
        nlines = int(180/dtheta)
        theta_grid = np.linspace(0., np.pi, nlines + 1)[1:-1]
        xc, yc = self.heal2ortho.transform(0., 0.)
        if onsphere == True:
            for ii in range(0, len(phi_grid)):
                phi_val = phi_grid[ii]
                phi_str = r'$ %s ^{\circ}$' % str(np.round(np.rad2deg(phi_val), decimals=decimals))[:-2]
                theta_val = zeropoint[1]
                phi_val -= np.deg2rad(shift[0])
                x, y = self.heal2ortho.transform(phi_val, theta_val)
                rotation_angle = 270. - np.rad2deg(np.arctan2((y-yc), (x-xc)))
                #x += shiftfractionphi[0]*(self.heal2ortho.xedges[-1] - self.heal2ortho.xedges[0])
                #y += shiftfractionphi[1]*(self.heal2ortho.yedges[-1] - self.heal2ortho.yedges[0])
                if x >= self.heal2ortho.xedges[0] and x <= self.heal2ortho.xedges[-1] and y >= self.heal2ortho.yedges[0] and y <= self.heal2ortho.yedges[-1]:
                    if ax is None:
                        if userotation == True:
                            plt.text(x, y, phi_str, rotation=rotation_angle, ha=ha, va=va, **kwargs)
                        else:
                            plt.text(x, y, phi_str, ha=ha, va=va, **kwargs)
                    else:
                        if userotation == True:
                            ax.text(x, y, phi_str, rotation=rotation_angle, ha=ha, va=va, **kwargs)
                        else:
                            ax.text(x, y, phi_str, ha=ha, va=va, **kwargs)

            for ii in range(0, len(theta_grid)):
                theta_val = theta_grid[ii]
                if lonlat == True:
                    theta_val = np.pi/2. - theta_val
                theta_str = r'$ %s ^{\circ}$' % str(np.round(np.rad2deg(theta_val), decimals=decimals))[:-2]
                theta_val = theta_grid[ii]
                phi_val = zeropoint[0]
                theta_val -= np.deg2rad(shift[1])
                if phi_val < 0.:
                    phi_val += 2.*np.pi
                elif phi_val >= 2.*np.pi:
                    phi_val -= 2.*np.pi
                x, y = self.heal2ortho.transform(phi_val, theta_val)
                rotation_angle = 270. - np.rad2deg(np.arctan2((y-yc), (x-xc)))
                #x += shiftfractiontheta[0]*(self.heal2ortho.xedges[-1] - self.heal2ortho.xedges[0])
                #y += shiftfractiontheta[1]*(self.heal2ortho.yedges[-1] - self.heal2ortho.yedges[0])
                if x >= self.heal2ortho.xedges[0] and x <= self.heal2ortho.xedges[-1] and y >= self.heal2ortho.yedges[0] and y <= self.heal2ortho.yedges[-1]:
                    if ax is None:
                        if userotation == True:
                            plt.text(x, y, theta_str, rotation=rotation_angle, ha=ha, va=va, **kwargs)
                        else:
                            plt.text(x, y, theta_str, ha=ha, va=va, **kwargs)
                    else:
                        if userotation == True:
                            ax.text(x, y, theta_str, rotation=rotation_angle, ha=ha, va=va, **kwargs)
                        else:
                            ax.text(x, y, theta_str, ha=ha, va=va, **kwargs)
        else:
            # Get Y-axis
            y = np.linspace(self.heal2ortho.yedges[0], self.heal2ortho.yedges[-1], interpaxis)
            x = self.heal2ortho.xedges[-1]*np.ones(interpaxis)
            z = np.sqrt(self.heal2ortho.radius**2. - (x**2. + y**2.))
            rr, phi, theta = coords.cart2sphere(x, y, z)
            phi, theta = coords.usphere_shift(phi, theta, self.heal2ortho.end_center[0], self.heal2ortho.end_center[1], self.heal2ortho.center[0], self.heal2ortho.center[1])

            if np.argmax(theta) != 0 and np.argmax(theta) != len(theta)-1:
                split = True
                inbetween = 'max'
            elif np.argmin(theta) != 0 and np.argmin(theta) != len(theta)-1:
                split = True
                inbetween = 'min'
            else:
                split = False
                inbetween = None

            if split == False:
                condition = np.where((theta_grid >= theta.min()) & (theta_grid <= theta.max()))[0]
                f = interpolate.interp1d(theta, y)
                y_ticks = f(theta_grid[condition])
                y_labels = coords.polar2lonlat(theta_grid[condition])
            else:
                if inbetween == 'min':

                    y1, theta1 = y[0:np.argmin(theta)], theta[0:np.argmin(theta)]

                    condition = np.where((theta_grid >= theta1.min()) & (theta_grid <= theta1.max()))[0]
                    f = interpolate.interp1d(theta1, y1)
                    y_ticks1 = f(theta_grid[condition])
                    y_labels1 = coords.polar2lonlat(theta_grid[condition])

                    y2, theta2 = y[np.argmin(theta):-1], theta[np.argmin(theta):-1]

                    condition = np.where((theta_grid >= theta2.min()) & (theta_grid <= theta2.max()))[0]
                    f = interpolate.interp1d(theta2, y2)
                    y_ticks2 = f(theta_grid[condition])
                    y_labels2 = coords.polar2lonlat(theta_grid[condition])

                elif inbetween == 'max':

                    y1, theta1 = y[0:np.argmax(theta)], theta[0:np.argmax(theta)]

                    condition = np.where((theta_grid >= theta1.min()) & (theta_grid <= theta1.max()))[0]
                    f = interpolate.interp1d(theta1, y1)
                    y_ticks1 = f(theta_grid[condition])
                    y_labels1 = coords.polar2lonlat(theta_grid[condition])

                    y2, theta2 = y[np.argmax(theta):-1], theta[np.argmax(theta):-1]

                    condition = np.where((theta_grid >= theta2.min()) & (theta_grid <= theta2.max()))[0]
                    f = interpolate.interp1d(theta2, y2)
                    y_ticks2 = f(theta_grid[condition])
                    y_labels2 = coords.polar2lonlat(theta_grid[condition])
                y_ticks = np.concatenate([y_ticks1, y_ticks2])
                y_labels = np.rad2deg(np.concatenate([y_labels1, y_labels2]))
            y_labels = np.round(y_labels, decimals=0).astype('int')

            # Get X-axis
            x = np.linspace(self.heal2ortho.xedges[0], self.heal2ortho.xedges[-1], interpaxis)
            y = self.heal2ortho.yedges[0]*np.ones(interpaxis)
            z = np.sqrt(self.heal2ortho.radius**2. - (x**2. + y**2.))
            rr, phi, theta = coords.cart2sphere(x, y, z)
            phi, theta = coords.usphere_shift(phi, theta, self.heal2ortho.end_center[0], self.heal2ortho.end_center[1], self.heal2ortho.center[0], self.heal2ortho.center[1])

            if np.argmax(phi) != 0 and np.argmax(phi) != len(phi)-1:
                split = True
                inbetween = 'max'
            elif np.argmin(phi) != 0 and np.argmin(phi) != len(phi)-1:
                split = True
                inbetween = 'min'
            else:
                split = False
                inbetween = None

            phi_grid = np.linspace(0., 2.*np.pi, int(360./20.)+1)[:-1]

            if split == False:
                condition = np.where((phi_grid >= phi.min()) & (phi_grid <= phi.max()))[0]

                f = interpolate.interp1d(phi, x)
                x_ticks = f(phi_grid[condition])
                x_labels = np.rad2deg(phi_grid[condition])

            else:
                if inbetween == 'min':

                    x1, phi1 = x[0:np.argmin(phi)], phi[0:np.argmin(phi)]

                    condition = np.where((phi_grid >= phi1.min()) & (phi_grid <= phi1.max()))[0]
                    f = interpolate.interp1d(phi1, x1)
                    x_ticks1 = f(phi_grid[condition])
                    x_labels1 = phi_grid[condition]

                    x2, phi2 = x[np.argmin(phi):-1], phi[np.argmin(phi):-1]

                    condition = np.where((phi_grid >= phi2.min()) & (phi_grid <= phi2.max()))[0]
                    f = interpolate.interp1d(phi2, x2)
                    x_ticks2 = f(phi_grid[condition])
                    x_labels2 = phi_grid[condition]

                elif inbetween == 'max':

                    x1, phi1 = x[0:np.argmax(phi)], phi[0:np.argmax(phi)]

                    condition = np.where((phi_grid >= phi1.min()) & (phi_grid <= phi1.max()))[0]
                    f = interpolate.interp1d(phi1, x1)
                    x_ticks1 = f(phi_grid[condition])
                    x_labels1 = phi_grid[condition]

                    x2, phi2 = x[np.argmax(phi):-1], phi[np.argmax(phi):-1]

                    condition = np.where((phi_grid >= phi2.min()) & (phi_grid <= phi2.max()))[0]
                    f = interpolate.interp1d(phi2, x2)
                    x_ticks2 = f(phi_grid[condition])
                    x_labels2 = phi_grid[condition]

                x_ticks = np.concatenate([x_ticks1, x_ticks2])
                x_labels = np.rad2deg(np.concatenate([x_labels1, x_labels2]))
            x_labels = np.round(x_labels, decimals=0).astype('int')

            if ax is None:
                plt.xticks(ticks=x_ticks, labels=x_labels, **kwargs)
                plt.yticks(ticks=y_ticks, labels=y_labels, **kwargs)
            else:
                ax.set_xticks(x_ticks)
                ax.set_xticklabels(x_labels, **kwargs)
                ax.set_yticks(y_ticks)
                ax.set_yticklabels(y_labels, **kwargs)


    def plot_polar_box(self, phi_min, phi_max, theta_min, theta_max, lonlat=False,
                 ax=None, divisions=100, **kwargs):
        """Plots a polar grid box.

        Parameters
        ----------
        phi_min : float
            Minimum phi-value of the box.
        phi_max : float
            Maximum phi-value of the box.
        theta_min : float
            Minimum theta-value of the box.
        theta_max : float
            Maximum theta-value of the box.
        lonlat : bool, optional
            Determines whether coordinates are in longitude and latitude convention.
        ax : class, optional
            Axis to plot on.
        divisions : int, optional
            Divisions in each line segment.
        """
        if lonlat == True:
            _t1, _t2 = theta_min, theta_max
            theta_min = np.pi/2. - _t2
            theta_max = np.pi/2. - _t1
        phi_box, theta_box = shapes.get_box(phi_min, phi_max, theta_min, theta_max, divisions=divisions)
        x, y = self.heal2ortho.transform(phi_box, theta_box)
        if ax is None:
            plt.plot(x, y, **kwargs)
        else:
            ax.plot(x, y, **kwargs)


    def finalize(self, insphere=True, ax=None, outeredge=True, edgecolor='k',
                 edgelinewidth=10, edgelength=1000, edgecenter=[0., 0.], **kwargs):
        """Finalize the orthographic plot.

        Parameters
        ----------
        heal2ortho : class
            For transformation.
        insphere : bool, optional
            If true then this means we are plotting as though we are looking from
            inside the sphere, as you would if your map is of the sky.
        ax : class, optional
            Axis to plot on.
        outeredge : bool, optional
            This will plot a circle defining the edge of the sphere.
        edgecolor : str, optional
            Color of the outeredge.
        edgelinewidth : float, optional
            Linewidth of the circle edge.
        edgelength : int, optional
            Length of the datapoints used to create the edge circle.
        edgecenter : list, optional
            Center of the outeredge circle.
        """
        if outeredge is True:
             plot_shapes.plot_circle(radius=self.heal2ortho.radius, center=edgecenter,
                                     length=edgelength, color=edgecolor,
                                     linewidth=edgelinewidth, ax=ax, **kwargs)
        if ax is None:
            if insphere == True:
                plt.xlim(self.heal2ortho.xedges[-1], self.heal2ortho.xedges[0])
            else:
                plt.xlim(self.heal2ortho.xedges[0], self.heal2ortho.xedges[-1])
            plt.ylim(self.heal2ortho.yedges[0], self.heal2ortho.yedges[-1])
        else:
            if insphere == True:
                ax.set_xlim(self.heal2ortho.xedges[-1], self.heal2ortho.xedges[0])
            else:
                ax.set_xlim(self.heal2ortho.xedges[0], self.heal2ortho.xedges[-1])
            ax.set_ylim(self.heal2ortho.yedges[0], self.heal2ortho.yedges[-1])
        if ax is None:
            plt.axis('off')
        else:
            ax.axis('off')
