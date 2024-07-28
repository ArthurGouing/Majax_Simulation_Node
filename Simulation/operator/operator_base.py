#################################################
# Copyright (C) 2025 Arthur Gouinguenet - All Rights Reserved
# This file is part of Majax Simulation Node project which is
# delivered under GNU General Public Liscense.
# For any questions or requests related to the use of this work
# please contact me directly at arthur.gouinguenet@free.fr
#############################################################

#### Library Import #### 
from abc import ABC, abstractmethod

#### Blender Import #### 
from bpy.types import NodeSocket

#### Local Import #### 
from Simulation.data.data_base import Data, Argument


class Operator(ABC):
    def __init__(self, name: str) -> None:
        # Unic ID of the operator
        self.id_name: str      = name
        # Ordered List of data used in input
        self.inputs: list[Argument] = list()
        # Oredered List of data writtent to output
        self.outputs: list[Argument] = list()
        # Controle Structure id_name where the operator live in
        self.parent: str = ""

    def set_parent(self, parent_name: str) -> None:
        self.parent = parent_name

    def add_input(self, socket: NodeSocket, intent: str, id_data: str, from_arg:str =None):
        self.inputs.append(Argument(socket, intent, id_data, from_arg))
    def add_output(self, socket: NodeSocket, intent: str, id_data: str, from_arg: str=None):
        self.outputs.append(Argument(socket, intent, id_data, from_arg))
        if socket.intent=="inout": # Move dans le argument constructor
            arg_out = self.outputs[-1]
            if not from_arg:
                arg_out.from_arg = socket.name.replace(" ", "_")+"_"+socket.node.name+"_in" # Sauf pour l'operator Simulation output

    def replace_output(self, socket_id_name: str, data: str):
        for socket in self.inputs:
            if socket.id_name==socket_id_name:
                socket.data = data

    def intputs_data(self, data_dict: dict[str, Data]) -> list[Data]: # Un yield eviterait des movements de data inutile
        inputs: list[Data] = list()
        for name in self.inputs:
            inputs.append(data_dict[name])
        return inputs

    def get_input(self, input_name: str)-> Data:
        for inp in self.inputs:
            if inp.id_name==input_name:
                return inp
    def get_output(self, output_name: str)-> Data:
        for out in self.outputs:
            if out.id_name==output_name:
                return out

    @abstractmethod
    def compute(self, data: dict[str, Data]) -> None:
        pass
