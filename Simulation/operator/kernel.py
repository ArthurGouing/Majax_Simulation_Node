#### Library Import #### 
import numpy as np
import re
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
        self.build_argument_dict()
        return error_msg

    def build_argument_dict(self):
        """ Read the kernel source to find which Data name is associate with which argument position in the kernel"""
        self.alias: dict[str, str] = dict()
        self.ker_argument_name: dict[int, str] = dict()
        start_read_arg = False

        lines = self.source.split("\n")
        for line in lines:
            # End of the definition of the kernel
            if re.search("{", line): 
                return
            
            # Read the alias
            if not start_read_arg:
                r = re.findall("\s*@alias@\s*(\w*)\s*=\s*(\w*)", line)
                if r:
                    self.alias.update({r[0][0]: r[0][1]})

            # Read the arguments
            if not start_read_arg:
                r = re.search("kernel\s*void.*\(", line)
                if r:
                    start_read_arg = True
                    line = line[r.span()[1]:] # on suprime tout ce qu'il y a avant le "("
                    arg_id = self.read_argument(line, 0)
            else: #  run over each arguments
                arg_id = self.read_argument(line, arg_id)

    def read_argument(self, line: str, arg_id: int) -> int: # return the arg_id
        """ Extract the name and usefull type information from kernel argument definition ('float *<name>' like string)"""
        arguments: str = line.split(",") # TODO: on peut faire un allfind au lieux de pré split

        for str_arg in arguments:
            # Buffer case
            r = re.search("global\s*(float|int)\s*\*", str_arg)
            if r :
                arg_name = re.search("\w*", str_arg[r.span()[1]:]).group()
                name = self.alias.get(arg_name, arg_name)
                split = name.split("_")
                object_name = split[0]+"_Buffers"
                buffer_name = "_".join(split[1:])
                arg_info = {"name": name}
                arg_info.update({"type": "buffer"})
                arg_info.update({"buffer": buffer_name})
                arg_info.update({"object": object_name})
                self.ker_argument_name.update({arg_id: arg_info})
                arg_id+=1
                continue

            # Scalar case
            r = re.findall("((const)?\s*(float|int)\s*)(\w*)", str_arg)
            if r:
                arg_name = r[0][3]
                name = self.alias.get(arg_name, arg_name)
                arg_info = {"name": name}
                arg_info.update({"type": "numpy"})
                arg_info.update({"object": name})
                self.ker_argument_name.update({arg_id: arg_info})
                arg_id+=1
                continue

            # Array parameters (Vector or Transform matrix)
            # TODO:
        return arg_id

    def compute(self, queue: OpenCLQueue, buffers: dict[Data]):
        if not self.worksize:
            buffer = [buf for name, buf in buffers.items() if name[-7:]=="Buffers"][0]
            self.compute_worksize(buffer.data) # i.e. Get le 1er buffer geometry inout

        # TODO: A chaque subit !!( très souvent !!!)
        # on a des test condition et des lecture de dictionnaire
        # Alors que une fois qu'on a trouvé le chemain, c'est tjrs le meme à chaque ité
        # Il faudrait que buffers contienne tous les buffers indiférement du OpenCLBuffer class
        # le buffer[name].data c'est le cl.Buffer
        for id, arg_info in self.ker_argument_name.items():
            object_name = arg_info["object"]
            if arg_info["type"]=="buffer":
                buffer_name = arg_info["buffer"]
                data = buffers[object_name].data.buffers[buffer_name]
                self.kernel.set_arg(id, data)
            elif arg_info["type"]=="numpy":
                data = buffers[object_name].data
                self.kernel.set_arg(id, data)

        # self.kernel.set_args(*buffers) # (initial idea)
        # Link data to kernel arguement
        # self.kernel.set_args(buffers[0].data.buffers["points"], buffers[1].data)
        # self.kernel.set_arg(0, buffers[0].data.buffers["points"])
        # self.kernel.set_arg(1, buffers[0].data.buffers["pt_var_velocity"])
        # self.kernel.set_arg(2, buffers[0].data.buffers["pt_var_l0"])
        # self.kernel.set_arg(3, buffers[0].data.buffers["pt_var_neighbor"])
        # Dt: TODO
        # self.kernel.set_arg(4, np.float32(0.0416)) # 1/24 !
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