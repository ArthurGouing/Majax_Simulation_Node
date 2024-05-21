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
    def __init__(self, name: str, source: str, method: str, expr: str=None) -> None:
        super().__init__(name)
        self.name = name
        self.kernel: cl.Kernel = None
        self.worksize = None
        self.worksize_method = method
        self.worksize_expr = expr
        self.source = source # open('Simulation/kernel/'+self.file_name).read()
        # TODO work size compute 

    def compile(self, context, options: str | list[str]=list()) -> str:
        # Compile here
        program = cl.Program(context, self.source).build(options=options)
        # There is 1 kernel per file i.e. by node kernel operator (logic)
        self.kernel = program.all_kernels()[0]
        # Get infor to print all the info to the log
        error_msg = "Error msg"
        device = context.get_info(cl.context_info.DEVICES)[0]
        print("DEVICE : ", device.name, device.vendor)
        print("STATUS: ", program.get_build_info(device, cl.program_build_info.STATUS))
        print("OPTIONS: ", program.get_build_info(device, cl.program_build_info.OPTIONS))
        print("LOG:", program.get_build_info(device, cl.program_build_info.LOG))
        print("Kernel:", program.all_kernels())
        print("")
        print(f" The kernel '{self.kernel.function_name}' take {self.kernel.num_args} arguments")
        return error_msg

    def compute(self, queue: OpenCLQueue, *buffers: Data):
        if not self.worksize:
            self.compute_worksize(buffers[0].data) # i.e. Get le 1er buffer geometry inout
        # self.kernel.set_args(*buffers) # (initial idea)
        # Link data to kernel arguement
        self.kernel.set_args(buffers[0].data.buffers["points"], buffers[1].data)
        event = cl.enqueue_nd_range_kernel(queue, self.kernel, self.worksize, None) # can specify local_work_size
    
    def compute_worksize(self, buffer: OpenCLBuffers):
        # Correct previous design error TODO:
        point_size = buffer.point_size[0]
        prim_size = buffer.prim_size[0]

        if self.worksize_method=='POINT':
            self.worksize = (point_size,)
        elif self.worksize_method=='PRIM':
            self.worksize = (prim_size,)
        elif self.worksize_method=='CUSTOM':
            self.worksize = eval(self.worksize_expr)
        print("Compute worksize: ", self.worksize)


    def delete(self) -> None:
        # A priori pas utilse pour les kernels, à se renseigner
        pass

class BlOpenCLKernelOperator(OpenCLKernelOperator):
    """Blender wrapper to provide Blender compatible constructor"""
    def __init__(self, node: Node) -> None:
        src = node.script.as_string() if node.script is not None else ""
        expr = node.work_group_expr if node.work_group_size=='CUSTOM' else None
        super().__init__(node.name, src, node.work_group_size, expr)