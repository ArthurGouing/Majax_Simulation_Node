# TODO create variable class, whith subclass for uniform var
# can be float, int, vector, 
# Uniform or for all point // all groupe ??
# Variable uniform et non-unform hérite de Variable
import numpy as np

class Variable():
    def __init__(self, value, uniform: bool, stationary: bool=True) -> None:

        # Bool to tell if a Buffer has to be created on the GPU
        self.uniform: bool = uniform
        self.stationary: bool = stationary

        # Convert to numpy, to be used by OpenCL
        if isinstance(value, float):
            self.value = np.float32(value)
        elif isinstance(value, int):
            self.value = np.int32(value)
        elif isinstance(value, list) or isinstance(value, tuple):
            value = np.array(value)
        else:
            self.value = value
        if isinstance(value, np.ndarray):
            if np.issubdtype(value.dtype, np.floating):
                self.value = value.astype(np.float32)
            elif np.issubdtype(value.dtype, np.integer):
                self.value = value.astype(np.int32)
            else:
                self.value = value