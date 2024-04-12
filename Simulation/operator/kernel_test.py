
#### Library Import #### 
import numpy as np
import pyopencl as cl

#### Blender Import #### 
from bpy.types import Node

#### Local Import #### 
from .operator_base import Operator
from Simulation.data.data_base import Data
from Simulation.queue_gpu import OpenCLQueue
from Simulation.data.buffer import OpenCLBuffer

# Queue ? quand est ce que le ker en a besoin ? init ? compute ?
# Et comment on indique le worksize ? 
# à priori un int à ce niveau, mais des paramétres genre n_vert/n_edge/n_faces peuvent apparaitre à plus haut niveau

# Source path ou source str ???

# From OpenCLKernel create 2 childs, 1 with custom soucefile, an other with defined sourcefile
# eq to 1 with customsourcefile, and the source file path is contained in Nodeupdate or whatever

class KernelTestOperator(Operator):
    def __init__(self, name: str, worksize: int) -> None:
        super().__init__(name)
        self.name = name
        self.kernel: cl.Kernel = None
        self.source: str = """
__kernel void ker(__global const float *a, __global float *b)
{
    int id = get_global_id(0);
    b[id] = a[id] + 0.1f;
}
"""
        self.worksize = worksize
        pass

    def compile(self, context, options: str | list[str]=list()) -> str:
        error_msg = "Error msg"
        program = cl.Program(context, self.source).build(options=options)
        self.kernel = program.ker # IMPORTANT TODO : the kernel must be named kernel to work !!!!
        return error_msg

    def compute(self, queue: OpenCLQueue, *buffers: Data) -> None:
        print("     Execute kernel ")
        self.kernel.set_args(*buffers)
        event = cl.enqueue_nd_range_kernel(queue, self.kernel, global_work_size=self.worksize) # can specify local_work_size


    def delete(self) -> None:
        # A priori pas utilse pour les kernels, à se renseigner
        pass

class BlKernelTestOperator(KernelTestOperator):
    """Blender wrapper to provide Blender compatible constructor"""
    def __init__(self, node: Node) -> None:
        queue = None
        src = node.script.as_string() if node.script is not None else ""
        super().__init__(node.name, queue, src, node.work_group_size)