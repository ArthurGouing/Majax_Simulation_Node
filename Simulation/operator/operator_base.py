# Base class for operator
# Operator correspond to a node, they will execute the operation when the graph is executed
print("Reload operator base")

#### Library Import #### 
from abc import ABC, abstractmethod

#### Blender Import #### 

#### Local Import #### 
from Simulation.data.data_base import Data

class Operator(ABC):
    def __init__(self, name: str) -> None:
        # Unic ID of the operator
        self.id_name: str      = name
        # Ordered List of data used in input
        self.inputs: list[str] = list()
        # Oredered List of data writtent to output
        self.outputs: list[str] = list()

    def add_input(self, args_id: str):
        self.inputs.append(args_id)
    def add_output(self, args_id: str):
        self.outputs.append(args_id)

    def find_input(self, data_dict: dict[str, Data]): # Un yield eviterait des movements de data inutile
        inputs: list[Data] = list()
        for name in self.inputs:
            inputs.append(data_dict[name])
        return inputs

    @abstractmethod
    def compute(self, *args: Data) -> None:
        pass
