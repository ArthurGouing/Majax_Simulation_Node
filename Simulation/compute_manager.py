# Gere les data, les opréation, calcul les graphs, etc
#### Blender Import ####
from bpy.types import Object

#### File Import ####
from .data import Data
from .operator import Operator

from .pre_process import PreProcessing
from .simulator import Simulator
from .post_process import PostProcessing

from .graph import ComputationGraph


class ComputeManager: # Client
    """
    Class which manage all the datas and the operation of the Majax computation
    """
    # Store all the operations of the computation
    ops: dict[str, Operator]
    # Store all the datas of the computation
    args: dict[str, Data]  # datas c'est mieux ?
    # SubManager for computation before the simulation loop
    pre_process: PreProcessing
    # SubManager for the simulation loop
    simulator: Simulator
    # SubManager for the computation at the end of each frame
    post_process: PostProcessing

    # Information about the computation
    state: str

    def __init__(self) -> None:
        """ Initialisation """
        self.state = "Initialisation"
        self.ops = dict()
        self.args = dict()
        self.pre_process = PreProcessing()
        self.post_process = PostProcessing()
        self.simulator = Simulator()

    def update_graph(self, new_graph: ComputationGraph) -> None:
        """ Change the inputs and operators according to the graphs. rebuild or change """
        self.state = "Updating graph"
        self.ops = new_graph.get_ops()
        self.args = new_graph.get_args()
        self.pre_process.update_graph(new_graph, self.ops)
        print("Pre proc: ", [i.id_name for i in self.pre_process.ordered_ops])
        self.simulator.update_graph(new_graph, self.ops, self.args)
        print("Sim:      ", [i.id_name for i in self.simulator.ordered_ops])
        self.post_process.update_graph(new_graph, self.ops)
        print("Post proc:", [i.id_name for i in self.post_process.ordered_ops])
        pass

    def compute(self, n_frame: int = None) -> None:
        """ Realise the computation """
        print("Compute !!!")
        # Init
        frame = 0
        # If OpenCL Kernel aren't compile, Compile all kernels i.e. all operator in the simulator

        # Computation before simulation loop
        self.pre_process.compute(self.args)

        # loop on frames
        while frame <= n_frame:
            print("Frame=", frame)
            # loop simulation on substep
            self.simulator.compute(self.args)

            # output data after each frame
            self.post_process.compute(self.args)
            frame += 1

        # Computation at the end of the simulation
        # A voir comment on peut faire ca et comment ca peut être utile
        # self.finalise_process.compute() #
        # Enfait ca seriait un geo node sur la simu cached
