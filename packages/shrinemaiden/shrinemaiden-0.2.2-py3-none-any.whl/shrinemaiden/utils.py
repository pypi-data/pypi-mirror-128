from typing import *
import numpy as np

def trim_data(data: np.ndarray, batch_size: int):
    """
    Trims out the extra data that does not fit into batches
    EX:
    dim, batch_size = 192, 50
    to
    dim, batch_size = 150, 50

    PARAMETERS
    ----------
    data: ndarray
      The data that you want to trim
    batch_size: int
      The batch size
    """
    extra = data.shape[0] % batch_size
    if (extra == 0):
        return data
    return data[:-extra]
