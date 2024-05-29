#### Library Import #### 
import numpy as np
import pyopencl as cl

#### Blender Import #### 
from bpy.types import Node

#### Local Import #### 
from .operator_base import Operator
from Simulation.data.data_base import Data
from Simulation.queue_gpu import OpenCLQueue
from Simulation.data.buffer import OpenCLBuffers

# Queue ? quand est ce que le ker en a besoin ? init ? compute ?
# Et comment on indique le worksize ? 
# à priori un int à ce niveau, mais des paramétres genre n_vert/n_edge/n_faces peuvent apparaitre à plus haut niveau

# Source path ou source str ???

# From OpenCLKernel create 2 childs, 1 with custom soucefile, an other with defined sourcefile
# eq to 1 with customsourcefile, and the source file path is contained in Nodeupdate or whatever

class KernelCopyOperator(Operator):
    def __init__(self, name: str, wait: bool, from_point: bool,buffer_type: str, var_name: str) -> None:
        super().__init__(name)
        self.name = name
        self.wait_for = wait
        self.buffer_type = buffer_type
        self.var_name = var_name
        if buffer_type=='POINT':
            self.buffer_name = "points"
        elif buffer_type=='PRIM':
            self.buffer_name = "primitives"
        elif buffer_type=='POINT_VAR':
            self.buffer_name = "pt_var_" + var_name
        elif buffer_type=='PRIM_VAR':
            self.buffer_name = "prim_var_" + var_name
        elif buffer_type=='GROUP':
            self.buffer_name = "group_" + var_name
        else:
            # TODO: 
            print("Error")
        if from_point:
            self.buffer_name_src = "points"
        else:
            self.buffer_name_src = self.buffer_name
        
        
    def compile(self, context, options: str | list[str]=list()) -> str:
        pass

    def compute(self, queue: cl.CommandQueue, buffers: dict[Data]) -> None:
        src = buffers[self.inputs[1].data].data.buffers[self.buffer_name_src]
        dest = buffers[self.inputs[0].data].data.buffers[self.buffer_name]
        event = cl.enqueue_copy(queue, dest, src)
        if self.wait_for:
            event.wait()


    def delete(self) -> None:
        # A priori pas utilse pour les kernels, à se renseigner
        pass

class BlKernelCopyOperator(KernelCopyOperator):
    """Blender wrapper to provide Blender compatible constructor"""
    def __init__(self, node: Node) -> None:
        super().__init__(node.name, node.wait, node.from_point, node.buffer, node.var_name)