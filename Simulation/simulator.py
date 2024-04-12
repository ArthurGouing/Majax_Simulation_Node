from typing import Optional
import numpy as np
import pyopencl as cl

from .operator.kernel import OpenCLKernelOperator
from .queue_gpu import OpenCLQueue
from .data.buffer import OpenCLBuffer
from .graph import compute_order
from .operator import Operator, BlSimInputOperator
from Simulation.data.data_base import Data


Kernel = OpenCLKernelOperator
Queue = OpenCLQueue | cl.CommandQueue
Buffer = OpenCLBuffer

class Simulator:
    # Parameters of the simulation : dt, n_substep, etc..
    parameters: dict[str, float | int | str] = dict()
    # All of Kernel to execute
    kernel: dict[str, Kernel] = list()  # Use iterator for this one ? Les Operator devront aussi hold les scripts en str pour pouvoir les compiler
    # All buffers for GPU and CPU
    buffers: dict[str, Buffer]    = dict()
    # Current time value
    time: float = 0
    # Occuped GPU memory
    memoryGPU: float
    # States of the simulation #["Initialisation", "Sending Data", "Receving Data", "Computing", "Waiting", "Closing", ...]
    state: str

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
        print("context: ", self.gpu_context.get_info(cl.context_info.DEVICES))
        print("Queue on :", self.queue.get_info(cl.command_queue_info.DEVICE))

        # Create the list of kernel
        # self.kernels = self.operators
        self.buffers: list[str] = list()
        self.kernels: list[Operator] = list()

    def __str__(self) -> str:
        text = f"{self.state} | GPU memory : {self.memoryGPU:.3f} Gb"
        return 

    def order(self, ops: dict[str, Operator], args: dict [str, Data]) -> None:
        """ Called when the graph is updated and eventually some parameters or changed """
        inputs: list[str] = ["BlSimInputOperator"]
        ouputs: list[str] = ["BlSimOutputOperator"]
        self.ordered_ops = compute_order(ops, args, input_ops_name=inputs, output_ops_name=ouputs)
        # On enlève les Sim inputs
        self.kernels = self.ordered_ops[1:-1] # == kernels

        # Store all GPU buffers
        self.buffers = sum([op.inputs for op in self.ordered_ops], list())

        print(self.buffers)

    def start_sim(self, args: dict[str, Data]) -> None:
        print("Simulator:")
        print("  start sim: create buffers and load the first buffers")
        # create siminputs buffers and load data
        # create all buffers of the simulations
        pass

    def init_buffer(self, args: dict[str, Data]) -> None:
        mf = cl.mem_flags
        for buff_name in self.inputs:
            # Faire la différence entre les data en output du SimInput, et les lier à leur geométrie respective (fin du nom, normalement)
            # Il faut aussi la taille des buffers, d'une maniètre ou d'une autre
            geo_size = 0
            arg = args[buff_name]
            arg.data = cl.Buffer(self.gpu_context, mf.READ_ONLY | mf.COPY_HOST_PTR, size=geo_size) # Cann directly load buffer
        pass

    def realloc_buffers(self, data: str | list[str]) -> None:
        """"
        Called at the 'Simulation Input Node'
        Prepare the geometry data for the GPU computation, i.e.
        Convert the input data to buffers and send them to the GPU 
        """
        # C'est une série d'opération (essentiellement buffer copy to gpu) on écrit rien d'OpenCL ici !!!
        pass

    def compile(self) -> str:
        """
        Compile the OpenCL script
        (Eventually template the script)
        and 
        """
        print("Compile OpenCL Code")
        for ker in self.kernels:
            error_msg = ker.compile(self.gpu_context)

        return error_msg

    def compute(self, args: dict[str, Data]) -> None:
        """
        Execute all the Kernels in the graph order on the GPU
        """
        # forward
        # n_substep = self.parameters["substep"]
        print("")
        print("Sub loop:")
        for t in range(self.n_substep):
            self.step_forward(args)

    def step_forward(self, args: dict[str, Data]) -> None:
        """
        Execute all the kernels for 1 step
        """
        for ker in self.kernels: # cf class _iter__
            self.state = f"Computing {ker.id_name}" + " | " # op.arg.inputs.get_mee
            # Retrieve arguements, and GPU context
            input_args = [args[input_id] for input_id in ker.inputs]
            print( "  "+self.state+"Inputs arguments: ", *[arg.id_name for arg in input_args], sep=", ")

            # Launch the kernel
            ker.compute(self.queue, *input_args)

    def end_frame(self, args: dict[str, Data]) -> None:
        """
        Send data back to CPU buffers before doing the post processing on CPU
        """
        print("  End frame: Send the computed data to the CPU, for post processing and printing")
        return
        simoutput_op = self.ordered_ops[-1]
        inputs = simoutput_op.inputs
        outputs = simoutput_op.outputs
        for inp, out in zip(inputs, outputs):
            data_d = args[inp]
            data_h = args[out]
            cl.enqueue_copy(self.queue, data_h, data_d)

    def read_results(self, result: str | list[str], frequency: int=1) -> None:
        """
        Called at the 'Simulation Output Node'
        Read the computed results from the GPU,
        Send GPU buffer to CPU buffer for the selected data. i.e. Update CPU bUffer.
        (eventually convert to Blender geometry)
        """
        # Est ce que les valeurs que l'on output sont renvoyé à l'input ? 
        # Oui car les datas / buffers peuvent changer de nom et de taille
        pass



