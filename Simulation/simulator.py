from typing import Optional
import numpy as np
import pyopencl as cl

from .operator.kernel import OpenCLKernelOperator
from .queue_gpu import OpenCLQueue
from .data.buffer import OpenCLBuffers
from .graph import compute_order
from .operator import Operator, BlSimInputOperator
from Simulation.data.data_base import Data
from Simulation.control_structure import ControlStructure


Kernel = OpenCLKernelOperator
Queue = OpenCLQueue | cl.CommandQueue
Buffer = OpenCLBuffers

class Simulator:
    # Parameters of the simulation : dt, n_substep, etc..
    # parameters: dict[str, float | int | str] = dict()
    # All of Kernel to execute
    # kernel: dict[str, Kernel] = list()  # Use iterator for this one ? Les Operator devront aussi hold les scripts en str pour pouvoir les compiler
    # All buffers for GPU and CPU
    # buffers: dict[str, Buffer]    = dict()
    # Current time value
    # time: float = 0
    # Occuped GPU memory
    # memoryGPU: float
    # States of the simulation #["Initialisation", "Sending Data", "Receving Data", "Computing", "Waiting", "Closing", ...]
    # state: str

    def __init__(self, op: BlSimInputOperator) -> None:
        """
        Init parameters : fps, dt,  initial time, last time, etc...
        Create OpenCL Context and find GPU device
        """
        # General variable init
        self.state    : str = "Initialisation"
        self.n_substep: int = op.n_substep
        self.dt       : float = op.fps/float(op.n_substep)

        # Queues where the computation can be done
        # platforms = cl.get_platforms()
        # self.gpu_context = cl.Context(dev_type=cl.device_type.ALL, properties=[(cl.context_properties.PLATFORM, platforms[0])])
        self.gpu_context = cl.create_some_context(interactive=False)
        self.queue    : Queue = cl.CommandQueue(self.gpu_context) # build queeu

        # Create the list of kernel
        # self.kernels = self.operators
        self.buffers: list[str] = list()
        self.kernels: list[Operator] = list()

    def __str__(self) -> str:
        text = f"{self.state} | GPU memory : {self.memoryGPU:.3f} Gb"
        return text

    def order(self, ops: dict[str, Operator], struct_ctrl: dict[str, ControlStructure], datas: dict [str, Data]) -> None:
        """ Called when the graph is updated and eventually some parameters or changed """
        inputs: list[str] = ["BlSimInputOperator"]
        ouputs: list[str] = ["BlSimOutputOperator"]
        self.ordered_ops = compute_order(ops, datas, input_ops_name=inputs, output_ops_name=ouputs)
        # Retreive Sim input and Sim output operators
        self.kernels = self.ordered_ops[1:-1] # == kernels

        # replace base operator by structure control flow
        # TODO: move that into 'compute_order' and correct it for pos_process and pre_process
        all_struct = list(struct_ctrl.values())
        while all_struct:
            # Find the lower structure level
            op_names = [op.id_name for op in self.ordered_ops] # as ordered_ops change at each loop, it must be recomputed
            for struct in all_struct:
                finded = False
                if set(struct.child_names).issubset(set(op_names)):
                    all_struct.remove(struct)
                    name = struct.id_name
                    struct = struct_ctrl[name] # useless Not needed as the list take the ptr
                    finded = True
                    break
            if not finded:
                print("Error")
                print("all_struct: ", all_struct)
                print("ordered_ops: ", self.ordered_ops)

            # Replace the childs by the structure controle
            index = 0
            while index < len(self.ordered_ops):
                op = self.ordered_ops[index]
                if op.parent!=name:
                    index+=1
                    continue
                del self.ordered_ops[index]
                # index = index + 1 - 1
                last_index = index
                struct.append(op) # Add child to the list of inner op # And sotre the positions where he belive

            # Insert the struct in the ops_list at the last moved_op index
            self.ordered_ops[:last_index] += [struct]

        # Store all GPU buffers in a list
        self.input_op = self.ordered_ops.pop(0)
        self.output_op = self.ordered_ops.pop(-1)

        # self.buffers = {datas[inp.data] for inp in sum([op.inputs for op in self.kernels], []) }


    def start_sim(self, datas: dict[str, Data]) -> None:
        # Create Sim_in and Sim_out buffers
        for inp, out in zip(self.input_op.inputs, self.input_op.outputs): 
            if inp.type != "Geometry":
                datas[out.data].data = datas[inp.data].data # TODO: copy inutile de data (negligeable) il faut plutot que la data passe en inout, pour éviter d'avoir 2 data  float, une sur la partie  CPU et une sur la partie GPU alors que l'on a besoin de ca que pour les geometries buffers
                continue
            geo = datas[inp.data].data
            # Create buffer from geo
            datas[out.data].data = OpenCLBuffers(self.gpu_context)
            datas[out.data].data.init_from_geo(geo)

        # Create intermediate buffers
        for ker in self.kernels:
            var_list = dict()
            for inp in ker.inputs:
                var_list.update({inp.name: datas[inp.data].data})

            for out in ker.outputs:
                if out.type=='Geometry Buffers' and out.intent=='out':
                    # Get the values to execut the expr_size
                    exec("size = "+ out.expr_size, var_list)
                    size = var_list["size"]
                    datas[out.data].data = OpenCLBuffers(self.gpu_context)
                    datas[out.data].data.init_void_buffer(size)

    def compile(self) -> str:
        """
        Compile the OpenCL script
        (Eventually template the script)
        and 
        """
        print("Compile OpenCL Code")
        error_msg = "0"
        for ker in self.kernels:
            error_msg = ker.compile(self.gpu_context)

        return error_msg

    def compute(self, datas: dict[str, Data]) -> None:
        """
        Execute all the Kernels in the graph order on the GPU
        """
        # forward
        # n_substep = self.parameters["substep"]
        for t in range(self.n_substep):
            self.step_forward(datas)

    def step_forward(self, datas: dict[str, Data]) -> None:
        """
        Execute all the kernels for 1 step
        """
        for op in self.ordered_ops:
            op.compute(self.queue, datas)

        return
        for ker in self.kernels: # cf class _iter__
            self.state = f"Computing {ker.id_name}" + " | " # op.arg.inputs.get_mee
            # Retrieve arguements, and GPU context
            # TODO: Trouver un moyen de chercher les arguments qu'une seule fois ?
            input_args: dict = {inp.name: datas[inp.data] for inp in ker.inputs}
            output_args: dict = {out.name: datas[out.data] for out in ker.outputs}
            input_args.update(output_args)
            # print( "  "+self.state+"Inputs arguments: ", *[arg.id_name for arg in (input_args+output_args)], sep=", ")

            # Launch the kernel
            ker.compute(self.queue, input_args) 

    def end_frame(self, args: dict[str, Data]) -> None:
        """
        Send data back to CPU buffers before doing the post processing on CPU
        """
        # Get sim output operators
        inputs = self.output_op.inputs
        outputs = self.output_op.outputs
        for inp, out in zip(inputs, outputs):
            data_d = args[inp.data].data
            data_h = args[out.data].data
            # send points
            cl.enqueue_copy(self.queue, data_h.points, data_d.buffers["points"])
            # send primitves TODO: this if don't work with numpy array
            if data_h.primitives.size:
                cl.enqueue_copy(self.queue, data_h.primitives, data_d.buffers["primitives"])
            if data_h.variables_point:
                for name, host_buff in data_h.variables_point.items():
                    if not host_buff.stationary:
                        cl.enqueue_copy(self.queue, host_buff.value, data_d.buffers[f"pt_var_{name}"])
            if data_h.variables_prim:
                for name, host_buff in data_h.variables_prim.items():
                    if not host_buff.stationary:
                        cl.enqueue_copy(self.queue, host_buff.value, data_d.buffers[f"prim_var_{name}"])
            if data_h.groups:
                for name, host_buff in data_h.groups.items():
                    cl.enqueue_copy(self.queue, host_buff, data_d.buffers[f"group_{name}"])

    def read_results(self, result: str | list[str], frequency: int=1) -> None: # useless
        """
        Called at the 'Simulation Output Node'
        Read the computed results from the GPU,
        Send GPU buffer to CPU buffer for the selected data. i.e. Update CPU bUffer.
        (eventually convert to Blender geometry)
        """
        # Est ce que les valeurs que l'on output sont renvoyé à l'input ? 
        # Oui car les datas / buffers peuvent changer de nom et de taille
        pass



