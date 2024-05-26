# Init package
print("Load Simulation package")

# Importation des modules
# from .compute_manager import ComputeManager
from .data import *
from .data import __all__ as data_class_list
from .operator import *
from .operator import __all__ as op_class_list

from .queue_gpu import OpenCLQueue

from .control_structure import *
from .control_structure import __all__ as cs_class_list

from .compute_manager import ComputeManager

# Déclaration des éléments à exposer lors de l'importation du package
__all__ = ['ComputationGraph',
           'ComputeManager',
           'OpenCLQueue']

__all__ += data_class_list + op_class_list + cs_class_list