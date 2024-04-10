# An operator which execute python code

#### Library Import #### 

#### Blender Import #### 
from bpy.types import Node

#### Local Import #### 
from .operator_base import Operator
from Simulation.data import Data

class PythonScriptOperator(Operator):
    def __init__(self, name: str, src: str) -> None:
        super().__init__(name)
        self.source = src

    def compute(self, *args: Data) -> None:
        print("Execute Python script node")
        return

class BlPythonScriptOperator(PythonScriptOperator):
    def __init__(self, node: Node) -> None:
        src = node.script.as_string() if node.script is not None else ""
        super().__init__(node.name, src)
    