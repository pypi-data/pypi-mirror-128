import numpy as np

from .. import utils


def rebin_1d_single_bin_weights(bin_edges, bin_min, bin_max):
    """Gets weights.

    Parameters
    ----------
    bin_edges : array
        Edges of the bins.
    bin_min : float
        Minimum edge for the new bin.
    bin_max : float
        Maximum edge for the new bin.
    """
    weights = np.zeros(len(bin_edges)-1)
    condition = np.where((bin_edges >= bin_min) & (bin_edges <= bin_max))[0]
    if len(condition) == 0:
        condition1 = np.where((bin_edges >= bin_min))[0]
        if len(condition1) != 0 and len(condition1) != len(bin_edges):
            weights[condition1[0]-1] = 1.
        else:
            # If we can't find any bins then we return a NaN
            return np.nan
    elif len(condition) == 1:
        # To ensure we are not looking at the edges
        if condition[0] > 0 and condition[0] < len(bin_edges)-1:
            weights[condition[0]] = (bin_edges[condition[0]] - bin_min)/(bin_edges[condition[0]] - bin_edges[condition[0]-1])
            weights[condition[0]+1] = (bin_max - bin_edges[condition[0]])/(bin_edges[condition[0]+1] - bin_edges[condition[0]])
        # To deal with edges
        elif condition[0] == 0:
            weights[condition[0]] = 1.
        elif condition[0] == len(bin_edges)-1:
            weights[condition[0]] = 1.
    else:
        # General case
        # Create weights equal to one
        w = np.ones(len(condition) + 1)
        index = np.array(np.ndarray.tolist(condition-1) + [condition[-1]])
        if condition[-1] == len(bin_edges)-1:
            w = w[:-1]
            index = index[:-1]
        elif condition[0] == 0:
            w = w[1:]
            index = index[1:]
        if condition[0] != 0:
            # Alter first weight to account for the fact that the new bin intersects the first bin.
            w[0] = (bin_edges[condition[0]] - bin_min)/(bin_edges[condition[0]] - bin_edges[condition[0]-1])
        if condition[-1] != len(bin_edges)-1:
            # Alter last weight to account for the fact that the new bin intesrsects the last bin.
            w[-1] = (bin_max - bin_edges[condition[-1]])/(bin_edges[condition[-1]] - bin_edges[condition[-1]-1])
        weights[index] = w
    return weights


def _rebin_1d_single_bin(bin_edges, data, bin_min, bin_max):
    """Rebins to a single bin.

    Parameters
    ----------
    bin_edges : array
        Edges of the bins.
    data : array
        Errors on the data values.
    bin_min : float
        Minimum edge for the new bin.
    bin_max : float
        Maximum edge for the new bin.
    """
    condition = np.where((bin_edges >= bin_min) & (bin_edges <= bin_max))[0]
    if len(condition) == 0:
        condition1 = np.where((bin_edges >= bin_min))[0]
        if len(condition1) != 0 and len(condition1) != len(bin_edges):
            return data[condition1[0]-1]
        else:
            # If we can't find any bins then we return a NaN
            return np.nan
    elif len(condition) == 1:
        # To ensure we are not looking at the edges
        if condition[0] > 0 and condition[0] < len(bin_edges)-1:
            w1 = (bin_edges[condition[0]] - bin_min)/(bin_edges[condition[0]] - bin_edges[condition[0]-1])
            w2 = (bin_max - bin_edges[condition[0]])/(bin_edges[condition[0]+1] - bin_edges[condition[0]])
            return (w1*data[condition[0]-1] + w2*data[condition[0]])/(w1+w2)
        # To deal with edges
        elif condition[0] == 0:
            return data[0]
        elif condition[0] == len(bin_edges)-1:
            return data[-1]
    else:
        # General case
        # Create weights equal to one
        w = np.ones(len(condition) + 1)
        index = np.array(np.ndarray.tolist(condition-1) + [condition[-1]])
        if condition[-1] == len(bin_edges)-1:
            w = w[:-1]
            index = index[:-1]
        elif condition[0] == 0:
            w = w[1:]
            index = index[1:]
        if condition[0] != 0:
            # Alter first weight to account for the fact that the new bin intersects the first bin.
            w[0] = (bin_edges[condition[0]] - bin_min)/(bin_edges[condition[0]] - bin_edges[condition[0]-1])
        if condition[-1] != len(bin_edges)-1:
            # Alter last weight to account for the fact that the new bin intesrsects the last bin.
            w[-1] = (bin_max - bin_edges[condition[-1]])/(bin_edges[condition[-1]] - bin_edges[condition[-1]-1])
        return np.sum(w*data[index])/np.sum(w)


def _rebin_1d_single_bin_sigma(bin_edges, sigma, bin_min, bin_max):
    """Rebins to a single bin.

    Parameters
    ----------
    bin_edges : array
        Edges of the bins.
    sigma : array, optional
        Errors on the data values.
    bin_min : float
        Minimum edge for the new bin.
    bin_max : float
        Maximum edge for the new bin.
    """
    condition = np.where((bin_edges >= bin_min) & (bin_edges <= bin_max))[0]
    lengths = bin_edges[1:] - bin_edges[:-1]
    if len(condition) == 0:
        condition1 = np.where((bin_edges >= bin_min))[0]
        if len(condition1) != 0 and len(condition1) != len(bin_edges):
            length = bin_max - bin_min
            new_sigma = sigma[condition1[0]-1]**2.
            new_sigma *= lengths[condition1[0]-1]/length
            new_sigma = np.sqrt(new_sigma)
            return new_sigma
        else:
            # If we can't find any bins then we return a NaN
            return np.nan
    elif len(condition) == 1:
        # To ensure we are not looking at the edges
        if condition[0] > 0 and condition[0] < len(bin_edges)-1:
            w1 = (bin_edges[condition[0]] - bin_min)/(bin_edges[condition[0]] - bin_edges[condition[0]-1])
            w2 = (bin_max - bin_edges[condition[0]])/(bin_edges[condition[0]+1] - bin_edges[condition[0]])
            l1 = bin_edges[condition[0]] - bin_min
            l2 = bin_max - bin_edges[condition[0]]
            if l1 != 0:
                new_sigma = (lengths[condition[0]-1]/l1)*(w1*sigma[condition[0]-1])**2.
            else:
                new_sigma = 0.
            if l2 != 0:
                new_sigma += (lengths[condition[0]]/l2)*(w2*sigma[condition[0]])**2.
            new_sigma /= (w1+w2)**2.
            new_sigma = np.sqrt(new_sigma)
            return new_sigma
        # To deal with edges
        elif condition[0] == 0:
            length = bin_max - bin_edges[0]
            new_sigma = sigma[0]**2.
            new_sigma *= lengths[0]/length
            new_sigma = np.sqrt(new_sigma)
            return new_sigma
        elif condition[0] == len(bin_edges)-1:
            length = bin_edges[-1] - bin_min
            new_sigma = sigma[-1]**2.
            new_sigma *= lengths[-1]/length
            new_sigma = np.sqrt(new_sigma)
            return new_sigma
    else:
        # General case
        # Create weights equal to one
        w = np.ones(len(condition) + 1)
        index = np.array(np.ndarray.tolist(condition-1) + [condition[-1]])
        if condition[-1] == len(bin_edges)-1:
            w = w[:-1]
            index = index[:-1]
        elif condition[0] == 0:
            w = w[1:]
            index = index[1:]
        length = lengths[index]
        if index[0] != 0:
            # Alter first weight to account for the fact that the new bin intersects the first bin.
            w[0] = (bin_edges[index[0]] - bin_min)/(bin_edges[index[0]] - bin_edges[index[0]-1])
            length[0] = bin_edges[index[0]] - bin_min
        if index[-1] != len(bin_edges)-1:
            # Alter last weight to account for the fact that the new bin intesrsects the last bin.
            w[-1] = (bin_max - bin_edges[index[-1]])/(bin_edges[index[-1]] - bin_edges[index[-1]-1])
            length[-1] = bin_max - bin_edges[index[-1]]
        condition2 = np.where(length > 0.)[0]
        index = index[condition2]
        w = w[condition2]
        length = length[condition2]
        new_sigma = (w*sigma[index])**2.
        new_sigma *= (lengths[index]/length)
        new_sigma = np.sum(new_sigma)/(np.sum(w)**2.)
        new_sigma = np.sqrt(new_sigma)
        return new_sigma


def rebin_1d(bin_edges, data, new_bin_edges, w=None, sigma=None):
    """Rebins 1 dimensional data into an arbitrarily defined new bins.

    Parameters
    ----------
    bin_edges : array
        Edges of the bins.
    data : array
        The value for each bin.
    new_bin_edges : array
        Edges of the new bins.
    w : array, optional
        Weights.
    sigma : array, optional
        Errors on the data values.
    """
    # Sanity checks
    assert len(bin_edges)-1 == len(data), "Bin edges and data are the wrong dimensions."
    assert utils.is_pos_monotonic(bin_edges) == True, "Bin edges are not positively monotonic."
    assert utils.is_pos_monotonic(new_bin_edges) == True, "New bin edges are not positively monotonic."
    if w is not None:
        assert len(data) == len(w), "Data and weights must be equal in size."
    if sigma is not None:
        assert len(data) == len(sigma), "Data and sigma must be equal in size."
    # Rebin using the rebin_1d_val function
    if w is None:
        data_new = np.array([_rebin_1d_single_bin(bin_edges, data, new_bin_edges[i], new_bin_edges[i+1]) for i in range(0, len(new_bin_edges)-1)])
    else:
        data_new = np.array([_rebin_1d_single_bin(bin_edges, data*w, new_bin_edges[i], new_bin_edges[i+1]) for i in range(0, len(new_bin_edges)-1)])
        data_new /= np.array([_rebin_1d_single_bin(bin_edges, w, new_bin_edges[i], new_bin_edges[i+1]) for i in range(0, len(new_bin_edges)-1)])
    if sigma is not None:
        if w is None:
            sigma_new = np.array([_rebin_1d_single_bin_sigma(bin_edges, sigma, new_bin_edges[i], new_bin_edges[i+1]) for i in range(0, len(new_bin_edges)-1)])
        else:
            sigma_new = np.array([_rebin_1d_single_bin_sigma(bin_edges, sigma*w, new_bin_edges[i], new_bin_edges[i+1]) for i in range(0, len(new_bin_edges)-1)])
            sigma_new /= np.array([_rebin_1d_single_bin_sigma(bin_edges, w, new_bin_edges[i], new_bin_edges[i+1]) for i in range(0, len(new_bin_edges)-1)])
    # Return rebinned data
    if sigma is None:
        return data_new
    else:
        return data_new, sigma_new
