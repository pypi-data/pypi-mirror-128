import numpy as np


def shuffle(sample):
    """Shuffles the ordering of a sample.

    Parameters
    ----------
    sample : array
        Input sample data.
    """
    u_r = np.random.random_sample(len(sample))
    sortind = np.argsort(u_r)
    return sample[sortind]


def random_draw(sample, size):
    """Draws a random sample from an input function, the algorithm ensures there
    can be no repeats.

    Parameters
    ----------
    sample : array
        Input sample data.
    size : int
        Size of the random draws.

    Returns
    -------
    randsamp : array
        Random subsample.
    """
    assert size < len(sample), "Size must be less than the input sample."
    u_r = np.random.random_sample(len(sample))
    sortind = np.argsort(u_r)
    randsamp = sample[sortind[:size]]
    return randsamp


def random_prob_draw(sample, prob, size=None):
    """Probabilistic draw from an input sample.

    Parameters
    ----------
    sample : array
        Input sample data.
    prob : array, optional
        The probability assigned to each sample.
    size : int, optional
        Size of the probabilistic draw.

    Returns
    -------
    randsamp : array
        Random subsample.
    """
    u_r = np.random.random_sample(len(sample))
    if size is None:
        cond = np.where(u_r <= prob)[0]
        randsamp = sample[cond]
        randsamp = shuffle(randsamp)
    else:
        assert size < len(sample), "Size must be less than the input sample."
        assert any(prob <= 0.) == False, "Probabilities assigned 0 must be removed."
        u_w = u_r/prob
        sortind = np.argsort(u_w)
        randsamp = sample[sortind[:size]]
        randsamp = shuffle(randsamp)
    return randsamp


def stochastic_integer_weights(weights):
    """Returns stochastic integer weights for an input weight. This is useful for
    point processes that require integer weights, where a non-integer weight can
    be achieved by superposition of many realisations.

    Parameters
    ----------
    weights : array
        Input weights.

    Returns
    -------
    weights_SI : array
        Stochastic integer weights.
    """
    if np.isscalar(weights) == True:
        u_r = np.random.random_sample(1)[0]
        weights_SI = np.ceil(weights)
        if u_r < weights_SI - weights:
            weights_SI = np.floor(weights)
    else:
        u_r = np.random.random_sample(len(weights))
        weights_SI = np.ceil(weights)
        cond = np.where(u_r < weights_SI - weights)
        weights_SI[cond] = np.floor(weights[cond])
    return weights_SI


def stochastic_binary_weights(weights):
    """Returns stochastic binary integer weights for an input weight. This is
    useful for point processes that require binary integer weights, where a
    non-integer weight can be achieved by superposition of many realisations.

    Parameters
    ----------
    weights : array
        Input weights.

    Returns
    -------
    weights_SB : array
        Stochastic binary weights.
    """
    weights_SI = stochastic_integer_weights(weights)
    weights_SB = np.copy(weights_SI)
    if np.isscalar(weights) == True:
        if weights_SI > 1:
            weights_SB = 1
    else:
        cond = np.where(weights_SI > 1)[0]
        weights_SB[cond] = 1
    return weights_SB
