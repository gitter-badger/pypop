import os
import numpy as np

from base_functions import *
from base_functions import _squeeze_and_check


# helper functions
def _generate_shift_vector(func, ndim, low, high, seed=None):
    """Generate a random shift vector of dimension `ndim`, sampled uniformly between
        `low` (inclusive) and `high` (exclusive).

    Note that the generated shift vector will be automatically stored in txt form for further use.

    :param func: function name, a `str` or `function` object.
    :param ndim: number of dimensions of the shift vector, an `int` scalar.
    :param low: lower boundary of the shift vector, a `float` scalar or array_like of floats.
    :param high: upper boundary of the shift vector, a `float` scalar or array_like of floats.
    :param seed: seed for random number generator, a `int` scalar.
    :return: shift vector, a `ndim`-d vector sampled uniformly in [`low`, `high`).

    https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.uniform.html
    """
    low, high = _squeeze_and_check(low), _squeeze_and_check(high)
    if hasattr(func, "__call__"):
        func = func.__name__
    data_folder = "pypop_benchmarks_input_data"
    if not os.path.exists(data_folder):
        os.mkdir(data_folder)
    data_path = os.path.join(data_folder, "shift_vector_" + func + "_dim_" + str(ndim) + ".txt")
    shift_vector = np.random.default_rng(seed).uniform(low, high, size=ndim)
    np.savetxt(data_path, shift_vector)
    return shift_vector


def _load_shift_vector(func, x, shift_vector=None):
    """Load the shift vector which needs to be generated in advance.
        When `None`, the shift vector should have been generated and stored in txt form in advance.

    :param func: function name, a `function` object.
    :param x: decision vector, array_like of floats.
    :param shift_vector: shift vector, array_like of floats.
    :return: shift vector, a 1-d `ndarray` of `dtype` `np.float64` with the same size as `x`.
    """
    x = _squeeze_and_check(x)
    if shift_vector is None:
        if (not hasattr(func, "pypop_shift_vector")) or (func.pypop_shift_vector.size != x.size):
            data_folder = "pypop_benchmarks_input_data"
            data_path = os.path.join(data_folder, "shift_vector_" + func.__name__ + "_dim_" + str(x.size) + ".txt")
            shift_vector = np.loadtxt(data_path)
            func.pypop_shift_vector = shift_vector
        shift_vector = func.pypop_shift_vector
    shift_vector = _squeeze_and_check(shift_vector)
    if shift_vector.shape != x.shape:
        raise TypeError("shift_vector should have the same shape as x.")
    if shift_vector.size != x.size:
        raise TypeError("shift_vector should have the same size as x.")
    return shift_vector
