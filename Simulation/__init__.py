# Init package
print("Load Simulation package")

# Importation des modules
# from .compute_manager import ComputeManager
from .data import *
from .data import __all__ as data_class_list
from .operator import *
from .operator import __all__ as ex_class_list

from .graph import ComputationGraph
from .compute_manager import ComputeManager
from .queue_gpu import OpenCLQueue

# Déclaration des éléments à exposer lors de l'importation du package
__all__ = ['ComputationGraph',
           'ComputeManager',
           'OpenCLQueue']

__all__ += data_class_list + ex_class_list