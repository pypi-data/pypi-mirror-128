# encoding: utf-8
# pylint: disable=C0103
"""
Onsets
======

Onsets detection
----------------

.. autosummary::
    :toctree: generated/

    detection

"""

import csv
import numpy as np

from . import util
from . import features

__all__ = ['detection']

def load_beats(labels_file, delimiter=',', times_col=0, labels_col=1):
    """Load annotated beats from text (csv) file.

    Parameters
    ----------
    labels_file : str
        name (including path) of the input file
    delimiter : str
        string used as delimiter in the input file
    times_col : int
        column index of the time data
    labels_col : int
        column index of the label data

    Returns
    -------
    beat_times : np.ndarray
        time instants of the beats
    beat_labels : list
        labels at the beats (e.g. 1.1, 1.2, etc)

    Examples
    --------


    """


