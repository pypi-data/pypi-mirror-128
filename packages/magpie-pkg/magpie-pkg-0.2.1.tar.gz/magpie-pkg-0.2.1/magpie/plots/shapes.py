import numpy
import matplotlib.pylab as plt

from .. import shapes


def plot_box(x_min, x_max, y_min, y_max, ax=None, divisions=100, **kwargs):
    """Plots a box.

    Parameters
    ----------
    x_min : float
        Minimum x-value of the box.
    x_max : float
        Maximum x-value of the box.
    y_min : float
        Minimum y-value of the box.
    y_max : float
        Maximum y-value of the box.
    ax : class, optional
        Axis to plot on.
    divisions : int, optional
        Divisions in each line segment.
    """
    x, y = shapes.get_box(x_min, x_max, y_min, y_max, divisions=divisions)
    if ax is None:
        plt.plot(x, y, **kwargs)
    else:
        ax.plot(x, y, **kwargs)


def plot_circle(radius=1., center=[0., 0.], length=1000, ax=None, **kwargs):
    """Plots a circle.

    Parameters
    ----------
    radius : float, optional
        Size of the circle.
    center : list, optional
        Center of the circle.
    length : int, optional
        Length of the datavector to create the circle.
    ax : class, optional
        Axis to plot on.
    """
    x, y = shapes.get_circle(radius, center=center, length=length)
    if ax is None:
        plt.plot(x, y, **kwargs)
    else:
        ax.plot(x, y, **kwargs)
