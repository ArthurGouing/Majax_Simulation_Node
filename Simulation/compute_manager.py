# Gere les data, les opréation, calcul les graphs, etc
#### Blender Import ####
from bpy.types import Object, Nodes, NodeLinks

#### File Import ####
from .data import Data
from .operator import Operator, BlSimInputOperator

from .pre_process import PreProcessing
from .simulator import Simulator
from .post_process import PostProcessing

from .operator import __dict__
op_class_list = [cl for n, cl in __dict__.items() if n[-8:]=="Operator"]

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
        self.simulators: list[Simulator] = list()


    def update_graph(self, bl_nodes: Nodes, bl_links: NodeLinks) -> None:
        """ Change the inputs and operators according to the graphs. rebuild or change """
        self.state = "Updating graph"
        # Build operators and datas
        self.ops, self.args = self.read_graph(bl_nodes, bl_links)

        # Create simulator for each simulation loops
        self.simulators = list()
        for op in self.ops.values():
            if isinstance(op, BlSimInputOperator):
                sim = Simulator(op)
                sim.order(self.ops, self.args)
                self.simulators.append(sim)
        print("Simulator:", [ op.id_name for op in self.simulators[0].ordered_ops])

        # Build the list of operator to execute in the correct order for Pre processing ops
        self.pre_process.order(self.ops, self.args)
        print("Pre proc: ", [i.id_name for i in self.pre_process.ordered_ops])

        # Build the list of operator to execute in the correct order for Post processing ops
        self.post_process.order(self.ops, self.args)
        print("Post proc:", [i.id_name for i in self.post_process.ordered_ops])
        # Move to the simulator init
        # self.simulator.order(self.ops, self.args) 
        # print("Sim:      ", [i.id_name for i in self.simulator.ordered_ops])


    def read_graph(self, bl_nodes: Nodes, bl_links: NodeLinks) -> tuple[dict[str, Operator], dict[str, Data]]:
        operators = dict()
        arguments = dict()
        for node in bl_nodes:
            if node.type=='FRAME':
                continue
            for op_class in op_class_list:
                if op_class.__name__==node.operator:
                    # Initialize Operator
                    operator = op_class(node)
                    operators.update({operator.id_name: operator})
                    break
            # Create Data slot for each output of the operator
            for socket in node.outputs:
                if socket.bl_idname=="NodeSocketVirtual" :
                    continue
                from_op_idname = operator.id_name
                argument = Data(socket, from_op_idname)
                arguments.update({argument.id_name: argument})
                # Store argument output of the operator
                operator.add_output(argument.id_name)

        # Link the data to the inputs of each operator
        for link in bl_links:
            # ReFind the data name
            input_data_name = link.from_socket.bl_idname[10:] + "_" + link.from_node.name
            # Find the operator to link with
            output_op_name = link.to_node.name
            operator = operators[output_op_name]
            operator.add_input(input_data_name)
        
        return (operators, arguments)


    def compile(self) -> None:
        [sim.compile() for sim in self.simulators]


    def compute(self, n_frame: int = None) -> None:
        """ Realise the computation """
        print("Compute !!!")
        # Init
        frame = 0
        # If OpenCL Kernel aren't compile, Compile all kernels i.e. all operator in the simulator

        # Computation before simulation loop
        self.pre_process.compute(self.args)

        # Init Simulators
        [sim.start_sim(self.args) for sim in self.simulators]

        # loop on frames
        while frame <= n_frame:
            print("Frame=", frame)
            # loop simulation on substep
            [sim.compute(self.args) for sim in self.simulators]

            [sim.end_frame(self.args) for sim in self.simulators]

            # output data after each frame
            self.post_process.compute(self.args)
            frame += 1

        # End simulators
        # End pre/post processing ?

        # Computation at the end of the simulation
        # A voir comment on peut faire ca et comment ca peut être utile
        # self.finalise_process.compute() #
        # Enfait ca seriait un geo node sur la simu cached
