from typing import Optional
import numpy as np

from .operator.kernel import OpenCLKernelOperator
from .queue_gpu import OpenCLQueue
from .data.buffer import OpenCLBuffer
from .graph import ComputationGraph
from .operator import Operator
from Simulation.data.data_base import Data


Kernel = OpenCLKernelOperator
Queue = OpenCLQueue
Buffer = OpenCLBuffer

class Simulator:
    # Parameters of the simulation : dt, n_substep, etc..
    parameters: dict[str, float | int | str] = dict()
    # Queues where the computation can be done
    queues: dict[str, Queue]           = dict()
    # All of Kernel to execute
    kernel: dict[str, Kernel] = list()  # Use iterator for this one ? Les Operator devront aussi hold les scripts en str pour pouvoir les compiler
    # All buffers for GPU and CPU
    buffers: dict[str, Buffer]    = dict()
    # Current time value
    time: float = 0
    # Frame var
    frame: int = 0
    start_frame: int = 0
    end_frame: int = 24
    # Occuped GPU memory
    memoryGPU: float
    # States of the simulation #["Initialisation", "Sending Data", "Receving Data", "Computing", "Waiting", "Closing", ...]
    state: str

    def __init__(self) -> None:
        """
        Init parameters : fps, dt,  initial time, last time, etc...
        Create OpenCL Context and find GPU device
        """
        self.state = "Initialisation"
        self.memoryGPU = 0
        pass

    def __str__(self) -> str:
        text = f"{self.state} | GPU memory : {self.memoryGPU:.3f} Gb"
        return 

    def update_graph(self, new_graph: ComputationGraph, ops: dict[str, Operator], args: dict [str, Data]) -> None:
        """ Called when the graph is updated and eventually some parameters or changed """
        inputs: list[str] = ["BlSimInputOperator"]
        ouputs: list[str] = ["BlSimOutputOperator"]
        self.ordered_ops = new_graph.compute_order(input_ops_name=inputs, output_ops_name=ouputs)
        # On enlève les Sim inputs et Sim ouptus
        self.ordered_ops = self.ordered_ops[1:-1]

        self.realloc_buffers(args)

    def realloc_buffers(self, data: str | list[str]) -> None:
        """"
        Called at the 'Simulation Input Node'
        Prepare the geometry data for the GPU computation, i.e.
        Convert the input data to buffers and send them to the GPU 
        """
        # C'est une série d'opération (essentiellement buffer copy to gpu) on écrit rien d'OpenCL ici !!!
        pass

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

    def compile(self) -> str:
        """
        Compile the OpenCL script
        (Eventually template the script)
        and 
        """
        error_msg: str = ""

        return error_msg

    def compute(self, args: dict[str, Data]) -> None:
        """
        Execute all the Kernels in the graph order on the GPU
        """
        # forward
        # n_substep = self.parameters["substep"]
        print("")
        print("Simulator: ")
        n_substep = 1
        for t in range(n_substep):
            self.step_forward(args)
        return

    def step_forward(self, args: dict[str, Data]) -> None:
        """
        Execute all the kernels for 1 step
        """
        for ker in self.ordered_ops: # cf class _iter__
            self.state = f"Computing {ker.id_name}" + " | " # op.arg.inputs.get_mee
            # Retrieve arguements, and GPU context
            queue = None # self.queues[0]
            input_args = [args[input_id] for input_id in ker.inputs]

            # Launch the kernel
            ker.compute(queue, *input_args)




