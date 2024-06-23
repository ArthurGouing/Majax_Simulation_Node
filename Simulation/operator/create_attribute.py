#############################################################
# Copyright (C) 2025 Arthur Gouinguenet - All Rights Reserved
# This file is part of Majax Simulation Node project which is
# delivered under GNU General Public Liscense.
# For any questions or requests related to the use of this work
# please contact me directly at arthur.gouinguenet@free.fr
#############################################################


#### Library Import ####
import numpy as np

#### Blender Import ####
from bpy.types import Node

#### Local Import #### 
from .operator_base import Operator
from Simulation.data.data_base import Data
from Simulation.data.geometry import Variable



class BlCreateAttributeOperator(Operator):
    def __init__(self, node: Node) -> None:
        super().__init__(node.name)
        # Name of the new attribute
        self.var_name = node.var_name
        # Type of the attribute
        self.var_type = node.var_type
        # Parameter of the variable attribute
        self.is_uniform = node.is_uniform
        self.is_stationary = node.is_stationary
        self.is_local_memory = node.is_local_memory

        # Size of the attribute
        self.is_vec = node.is_vec
        # Per element size
        self.size = node.size
        # nb of all element for none uniform variables
        self.element_type = node.element_type
        # element type

    def compute(self, *args: Data) -> None:
        geo = args[0].data
        print("geo name", self.inputs[0].name)
        var_list = {self.inputs[0].name : geo}
        # Get locale size
        if self.is_vec:
            exec("local_size = "+ self.size, var_list)
            local_size = var_list["local_size"]
        else:
            if self.var_type=="VECTOR":
                local_size = 4
            elif self.var_type=="TRANSFORMATION":
                local_size = 16
            elif self.var_type=='ROTATION':
                local_size = 9
            else: 
                local_size = 1
        #  Get total size
        if not self.is_uniform:
            if self.element_type=='POINT':
                tot_size = geo.points.shape[0]
            elif self.element_type=='PRIM':
                tot_size = geo.primitives.shape[0]
        else:
            tot_size = 1

        # Build value
        el_value = local_size * [0]
        value = np.array(tot_size * el_value)
        print("el type:", self.element_type)
        print("is vec:", self.is_vec)
        print("id unif", self.is_uniform)
        print(local_size, tot_size)
        print(value, len(value))

        if self.var_type=="DOUBLE":
            dtype = np.double
        elif self.var_type=="INT":
            dtype = np.int32
        else:
            dtype = np.single

        if self.is_local_memory:
            var = Variable(size=local_size*tot_size, uniform=self.is_uniform, stationary=self.is_stationary, dtype=dtype)
        else:
            var = Variable(value=value, uniform=self.is_uniform, stationary=self.is_stationary, dtype=dtype)

        # Create the attribute into the geometry
        geo.update_variable(self.var_name, var)
        return
