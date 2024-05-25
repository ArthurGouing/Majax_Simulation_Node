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

class KernelTestOperator(Operator):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.name = name
        self.kernel: cl.Kernel = None
        self.file_name: str = "Test.cl"
        self.source = open('Simulation/kernel/'+self.file_name).read()
        pass

    def compile(self, context, options: str | list[str]=list()) -> str:
        error_msg = "Error msg"
        program = cl.Program(context, self.source).build(options=options)
        device = context.get_info(cl.context_info.DEVICES)[0]
        print("DEVICE : ", device.name, device.vendor)
        print("STATUS: ", program.get_build_info(device, cl.program_build_info.STATUS))
        print("OPTIONS: ", program.get_build_info(device, cl.program_build_info.OPTIONS))
        print("LOG:", program.get_build_info(device, cl.program_build_info.LOG))
        print("Kernel:", program.all_kernels())
        self.kernel = program.all_kernels()[0] 
        print("")
        print(f" The kernel '{self.kernel.function_name}' take {self.kernel.num_args} arguments")
        return error_msg

    def compute(self, queue: cl.CommandQueue, *buffers: Data) -> None:

        if self.file_name=='Test_2.cl':
            self.worksize = tuple([buffers[0].data.prim_size[0]])
            self.kernel.set_args(buffers[0].data.buffers["points"], buffers[0].data.buffers["primitives"])
        else:
            self.worksize = tuple([1521])
            self.kernel.set_args(buffers[0].data.buffers["points"])
        event = cl.enqueue_nd_range_kernel(queue, self.kernel, self.worksize, None) # can specify local_work_size


    def delete(self) -> None:
        # A priori pas utilse pour les kernels, à se renseigner
        pass

class BlKernelTestOperator(KernelTestOperator):
    """Blender wrapper to provide Blender compatible constructor"""
    def __init__(self, node: Node) -> None:
        super().__init__(node.name)