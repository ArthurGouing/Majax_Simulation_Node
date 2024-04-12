# Read data object from Blenderfile and convert them to Geometry data type
# Write solution Geometry to the selected Blender Object 

#### Library Import #### 

#### Blender Import #### 
from bpy.types import Object, Node
from Simulation.data.data_base import Data

#### Local Import #### 
from .operator_base import Operator

class BlExportGeoOperator(Operator):
    obj: Object
    # Static attribute
    id: int = 0

    def __init__(self, node: Node) -> None:
        super().__init__(node.name)
        self.obj = node.obj

    def compute(self, *args: Data) -> None:
        print("     Compute Export geo")
        return