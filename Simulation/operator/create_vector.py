#### Library Import ####
import numpy as np

#### Blender Import #### 
from bpy.types import Node

#### Local Import #### 
from .operator_base import Operator
from Simulation.data.data_base import Data


class BlCreateVectorOperator(Operator):
    def __init__(self, node: Node) -> None:
        super().__init__(node.name)
        self.value = np.array(list(node.value)+[int(node.v_type)])


    def compute(self, *args: Data) -> None:
        print("     Create float data")
        # Create the value and store it in the data dict
        args[0].data = self.value
        # set size ??