#### Library Import #### 
import numpy as np
import re
import pyopencl as cl
from time import perf_counter

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
    def __init__(self, name: str, source: str, method: str, wait: bool, expr: str=None) -> None:
        super().__init__(name)
        self.name = name
        self.kernel: cl.Kernel = None
        self.worksize = None
        self.worksize_method = method
        self.worksize_expr = expr
        self.wait_for = wait
        self.source = source # open('Simulation/kernel/'+self.file_name).read()
        # associate kernel argument id with data id
        self.argument: dict = dict()
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
                r = re.search("kernel\s*void\s*\w*\s*\(", line)
                if r:
                    start_read_arg = True
                    line = line[r.span()[1]:] # on suprime tout ce qu'il y a avant le "("
                    arg_id = self.read_argument(line, 0)
            else: #  run over each arguments
                arg_id = self.read_argument(line, arg_id)

    def read_argument(self, line: str, arg_id: int) -> int: # return the arg_id
        """ Extract the name and usefull type information from kernel argument definition ('float *<name>' like string)"""
        line = line.split("//")[0]
        arguments: str = line.split(",") # TODO: on peut faire un allfind au lieux de pré split

        for str_arg in arguments:
            # Buffer case
            # str_arg = (global|local|...) (float|int|...) name
            r = re.findall("\s*(\w*)\s*(\w+)\s*(\*)(\w+)", str_arg) 
            if r:
                arg_name = r[0][3]
                name = self.alias.get(arg_name, arg_name)
                split = name.split("_")
                object_name = split[0]
                buffer_name = "_".join(split[1:])
                arg_info = {"name": name}
                arg_info.update({"type": "buffer"})
                data_id_list = [arg.data for arg in sum([self.inputs, self.outputs], []) if arg.name== object_name]
                if not data_id_list:
                    print(f"Error: '{object_name}' not finded in {[arg.name for arg in sum([self.inputs, self.outputs], [])]} while processing {str_arg}")
                data_id = data_id_list[0]
                arg_info.update({"data_id": data_id})
                arg_info.update({"buffer": buffer_name})
                self.ker_argument_name.update({arg_id: arg_info})
                arg_id+=1
                continue

            r = re.findall("\s*(\w+)\s*(\*)?(\w+)", str_arg) 
            if r:
                arg_name = r[0][2]
                name = self.alias.get(arg_name, arg_name)
                arg_info = {"name": name}
                arg_info.update({"data_id": name})
                arg_info.update({"type": "numpy"})
                self.ker_argument_name.update({arg_id: arg_info})
                arg_id+=1
                continue

            # Array parameters (Vector or Transform matrix)
            # TODO:
        return arg_id

    def compute(self, queue: OpenCLQueue, buffers: dict[str, Data]): # buffers=compute_manager.datas
        if not self.worksize:
            buffer = [buf for buf in buffers.values() if buf.data_type=="Buffers"][0]
            self.compute_worksize(buffer.data) # i.e. Get le 1er buffer geometry inout

        # TODO: A chaque subit !!( très souvent !!!) (~10% pour 250 elements)
        # on a des test condition et des lecture de dictionnaire
        # Alors que une fois qu'on a trouvé le chemain, c'est tjrs le meme à chaque ité
        # Il faudrait que buffers contienne tous les buffers indiférement du OpenCLBuffer class
        # le buffer[name].data c'est le cl.Buffer
        for id, arg_info in self.ker_argument_name.items():
            data_name = arg_info["data_id"]
            # print(f"add {object_name} {arg_info.get('buffer', '')} to {id}")
            if arg_info["type"]=="buffer":
                buffer_name = arg_info["buffer"]
                data = buffers[data_name].data.buffers[buffer_name]
                self.kernel.set_arg(id, data)
            elif arg_info["type"]=="numpy":
                data = buffers[data_name].data
                self.kernel.set_arg(id, data)
        # TODO: des msg d'erreur clair !

        # Launch the kernel
        event = cl.enqueue_nd_range_kernel(queue, self.kernel, self.worksize, None) # can specify local_work_size
        if self.wait_for:
            event.wait()
    
    def compute_worksize(self, buffer: OpenCLBuffers):
        # Correct previous design error TODO:
        point_size = buffer.point_size
        point_shape = buffer.point_shape
        prim_size = buffer.prim_size
        prim_shape = buffer.prim_shape

        if self.worksize_method=='POINT':
            self.worksize = (point_shape[0],)
        elif self.worksize_method=='PRIM':
            self.worksize = (prim_shape[0],)
        elif self.worksize_method=='CUSTOM':
            self.worksize = eval(self.worksize_expr)


    def delete(self) -> None:
        # A priori pas utilse pour les kernels, à se renseigner
        pass

class BlOpenCLKernelOperator(OpenCLKernelOperator):
    """Blender wrapper to provide Blender compatible constructor"""
    def __init__(self, node: Node) -> None:
        if node.from_file:
            with open(node.script.filepath, 'r') as f:
                src = f.read()
        else:
            src = node.script.as_string() if node.script is not None else ""
        expr = node.work_group_expr if node.work_group_size=='CUSTOM' else None
        super().__init__(node.name, src, node.work_group_size, node.wait, expr)