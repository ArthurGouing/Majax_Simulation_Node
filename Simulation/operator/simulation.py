# Simulation operator qui tiens les arguments d'entrée et de sortie
# Il permet de mettre un marqueur de la node siminput dans l' ordered liste 

#### Library Import #### 

#### Blender Import #### 
from bpy.types import Node

#### Local Import #### 
from .operator_base import Operator
from Simulation.data.data_base import Data

class BlSimInputOperator(Operator):
    # Static attribute
    id: int = 0

    def __init__(self, node: Node) -> None:
        super().__init__(node.name)
        self.n_substep = node.substep
        self.fps = node.fps
        pass

    def compute(self, *args: Data) -> None:
        print("     Sim input, should not be executed")
        return

class BlSimOutputOperator(Operator):
    # Static attribute
    id: int = 0

    def __init__(self, node: Node) -> None:
        super().__init__(node.name)
        pass

    def compute(self, *args: Data) -> None:
        print("     Sim output, should not be executed")
        return
