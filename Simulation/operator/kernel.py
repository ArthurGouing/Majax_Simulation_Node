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

class OpenCLKernelOperator(Operator):
    source: str
    queue: cl.CommandQueue
    kernel: cl.Kernel
    size = 256
    # Static attribute
    id: int = 0

    def __init__(self, name: str, queue: cl.CommandQueue, source: str, worksize: int) -> None:
        super().__init__(name)
        self.queue = queue
        self.source = source # or extract from source_path
        self.worksize = worksize
        pass

    def compile(self, options: str | list[str]=list()) -> None:
        program = cl.Program(self.context, self.source).build(options=options)
        self.kernel = program.ker # IMPORTANT TODO : the kernel must be named kernel to work !!!!
        pass

    def compute(self, queue: OpenCLQueue, *buffers: Data):
        print("     Execute kernel ")
        return
        self.kernel.set_args(*buffers)
        event = cl.enqueue_nd_range_kernel(queue, self.kernel, self.worksize)

    def delete(self) -> None:
        # A priori pas utilse pour les kernels, à se renseigner
        pass

class BlOpenCLKernelOperator(OpenCLKernelOperator):
    """Blender wrapper to provide Blender compatible constructor"""
    def __init__(self, node: Node) -> None:
        queue = None
        src = node.script.as_string() if node.script is not None else ""
        super().__init__(node.name, queue, src, node.work_group_size)