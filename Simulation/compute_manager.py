# Gere les data, les opréation, calcul les graphs, etc
#### Libraries Import ####
from time import perf_counter
#### Blender Import ####
from bpy.types import Nodes, NodeLinks

#### File Import ####
from .data import Data
from .operator import Operator, BlSimInputOperator, BlSimOutputOperator
from .control_structure import ControlStructure, BlControlStructureLoop, BlControlStructureCondition

from .pre_process import PreProcessing
from .simulator import Simulator
from .post_process import PostProcessing

from Blender_ui.Nodes.simulation_input import SimInputNode
from Blender_ui.Nodes.simulation_output import SimOutputNode

from .operator import __dict__
op_class_list = [cl for n, cl in __dict__.items() if n[-8:]=="Operator"] # == __dict__["__all__"] == from .operator import __all__ as class_list_all

class ComputeManager: # Client
    """
    Class which manage all the datas and the operation of the Majax computation
    """

    # Information about the computation
    state: str

    def __init__(self) -> None:
        """ Initialisation """
        self.state = "Initialisation"
        # Store all the operations of the computation
        self.ops: dict[str, Operator] = dict()
        # Store all controle structure of the computation (For loop, and conditions)
        self.struct_ctrl: dict[str, ControlStructure] = dict()
        # Store all the datas of the computation
        self.args: dict[str, Data] = dict()
        # SubManager for computation before the simulation loop
        self.pre_process = PreProcessing()
        # SubManager for the simulation loop
        self.simulators: list[Simulator] = list()
        # SubManager for the computation at the end of each frame
        self.post_process = PostProcessing()


    def update_graph(self, bl_nodes: Nodes, bl_links: NodeLinks) -> None:
        """ Change the inputs and operators according to the graphs. rebuild or change """
        self.state = "Updating graph"
        # Build operators and datas
        self.ops, self.struct_ctrl, self.args = self.read_graph(bl_nodes, bl_links)

        # Create simulator for each simulation loops
        self.simulators = list()
        for op in self.ops.values():
            if isinstance(op, BlSimInputOperator):
                sim = Simulator(op) 
                sim.order(self.ops, self.struct_ctrl, self.args)
                self.simulators.append(sim)

        # Build the list of operator to execute in the correct order for Pre processing ops
        self.pre_process.order(self.ops, self.args)

        # Build the list of operator to execute in the correct order for Post processing ops
        self.post_process.order(self.ops, self.args)

        # Print ordered operation lists for each step
        print("Pre proc: ", [i.id_name for i in self.pre_process.ordered_ops])
        for sim in self.simulators:
            print(f"Simulator ({sim.queue.device.name}):", [ op.id_name for op in sim.ordered_ops])
        print("Post proc:", [i.id_name for i in self.post_process.ordered_ops])

    def read_graph(self, bl_nodes: Nodes, bl_links: NodeLinks) -> tuple[dict[str, Operator], dict[str, Data]]:
        t_start = perf_counter()
        operators = dict()
        control_structure = dict()
        datas = dict()
        simin_outputs = dict()

        oredered_node = list()
        ordered_ops = list()

        # Build one operator for each node
        for node in bl_nodes:
            if node.type=='FRAME':
                if node.operator == 'LOOP':
                    struct = BlControlStructureLoop(node)
                    control_structure.update({struct.id_name: struct})
                    continue
                elif node.operator=='IF':
                    struct = BlControlStructureCondition(node)
                    control_structure.update({struct.id_name: struct})
                    continue
                else:
                    continue
            # Create Operators
            for op_class in op_class_list:
                if op_class.__name__==node.operator:
                    # Initialize Operator
                    operator = op_class(node)
                    operators.update({operator.id_name: operator})
                    ordered_ops.append(operator.id_name)
                    oredered_node.append(node)
                    break
        
        # Build parent name for frame
        for name, struct in control_structure.items():
            parent_struct = control_structure.get(struct.parent, None)
            if parent_struct:
                parent_struct.append_name(name)

        # Build the data from 'out' sockets
        for op_name, node in zip(ordered_ops, oredered_node):
            # Get the operator
            operator = operators[op_name]
            # Store node parent information (for control structures)
            if node.parent:
                if node.parent.operator!='NOTE':
                    control_structure[node.parent.name].append_name(op_name)
                    operator.set_parent(node.parent.name)
            # Create output arguments and datas
            for socket in node.outputs:
                if socket.bl_idname=="MajaxSocketBase" :
                    continue
                # Don't need to generate data for the last buffer because it is the same as the first buffer of the loop
                if socket.links:
                    if isinstance(socket.links[0].to_node, SimOutputNode):
                        operator.add_output(socket, "out", "")
                        continue

                # Create and store data for intent out data (i.e. not the inout)
                if socket.intent=="out":
                    from_op_idname = operator.id_name
                    data = Data(socket, from_op_idname)
                    datas.update({data.id_name: data})
                    operator.add_output(socket, "out", data.id_name)
                    # Store outputs of the SimulationInputOperator TODO: don't work with several SimLoop !!!
                    if socket.links: 
                        if isinstance(socket.links[0].from_node, SimInputNode): # 106-107 eq to node == SimInput...
                            simin_outputs.update({data.name: data.id_name})
                # Manage the case of the SimOutput operator
                elif isinstance(operator, BlSimOutputOperator):
                    # Get SimInputNode name
                    for op in operators.values():
                        if isinstance(op, BlSimInputOperator): # TODO: Don't manage several Sim Loop
                            op_name = op.id_name
                            break
                    # Socket name must be the same by construction
                    from_arg_id = socket.name.replace(" ","_") +"_"+ op_name +"_in"
                    operator.add_output(socket, "out", "", from_arg_id)
                # Create outputs where the argument is intent 'inout' (link to the data later)
                else:
                    operator.add_output(socket, "out", "")

            # Create operator inputs arguments (link to the data later)
            for socket in node.inputs:
                # Ignore virtual sockets
                # if socket.bl_idname=="NodeSocketVirtual":
                if not socket.is_linked or socket.bl_idname=="MajaxSocketBase":
                     continue
                # Find from_arg
                link = socket.links[0] # only 1 link coz input
                from_arg = link.from_socket.name.replace(" ", "_") + "_" + link.from_node.name + "_out"
                # Add input
                operator.add_input(socket, "in", "", from_arg)

        # Link the data to the inputs of each operator and the "inout" outputs
        for link in bl_links:
            # Fill all Inputs arguments: arg
            to_op = operators[link.to_node.name]
            arg = to_op.get_input(link.to_socket.name.replace(" ","_")+"_"+to_op.id_name+"_in")
            op = operators[link.from_node.name]
            from_arg = op.get_output(link.from_socket.name.replace(" ","_")+"_"+op.id_name+"_out")
            id_data = from_arg.data
            if from_arg.intent=="inout": # or not id_data
                from_arg_origin = from_arg
            else:
                from_arg_origin = None
            # Recursive parcour of the 'inout' argument until reach a 'out' argument which contain a data
            while not id_data:
                # Work on the precedant link
                # from_arg is an output. if intent=inout(==no id_data), find the input associate with
                for inp in sum([op.inputs for op in operators.values()], []):
                    if inp.id_name==from_arg.from_arg:
                        to_arg = inp
                        break
                op = operators[to_arg.from_op] # get operator which the data come from
                from_arg = op.get_output(to_arg.from_arg)
                id_data = from_arg.data

            # Update data
            # Fill data of the to_argument of the link, of type 'in' or 'inout'
            arg.data = id_data
            # Fill data of the from_argument of the link, of type 'inout'
            if from_arg_origin: # ne devrait pas exister !!!
                from_arg_origin.data = id_data

            # Reste le cas du lien entre le dernier kernel et le Simoutput

        print("Control Structure:")
        print(*control_structure.keys(), sep="\n")

        t_end = perf_counter()
        print(f"\nReading Graph time: {(t_end-t_start)*1000:.3f} ms ({t_end-t_start:f} s)")
        print("")
        return (operators, control_structure, datas)


    def compile(self) -> None:
        t_start = perf_counter()
        [sim.compile() for sim in self.simulators]
        t_end = perf_counter()
        print(f"\nCompilation time: {(t_end-t_start)*1000:.3f} ms ({t_end-t_start:f} s)")
        print("")

        err_type = ""
        err_msg = ""
        return [err_type, err_msg]


    def init_compute(self, n_frame: int = None) -> None:
        """ Realise the computation """
        print("  --- Init computation ---")
        # Init
        # If OpenCL Kernel aren't compile, Compile all kernels i.e. all operator in the simulator

        # Computation before simulation loop
        t_start = perf_counter()
        self.pre_process.compute(self.args)
        t_end = perf_counter()
        print(f"\nPre Processing time: {(t_end-t_start)*1000:.3f} ms ({t_end-t_start:f} s)")
        print("")

        # Init Simulators (Load GPU buffers)
        t_start = perf_counter()
        [sim.start_sim(self.args) for sim in self.simulators]
        t_end = perf_counter()
        print(f"\nLoading GPU Data time: {(t_end-t_start)*1000:.3f} ms ({t_end-t_start:f} s)")
        print("")

        # loop on frames
        # while frame <= n_frame:
    def step_forward(self):
        # loop simulation on substep
        print("  --- Compute simulation loop ---")
        # Kernel computation
        # t_start = perf_counter()
        [sim.compute(self.args) for sim in self.simulators]
        # t_end = perf_counter()
        # print(f"\nGPU Loop Computation time: {(t_end-t_start)*1000:.3f} ms ({t_end-t_start:f} s)")
        # print("")

        # Transfer data back on the CPU
        print("  --- Send data back to GPU ---")
        # t_start = perf_counter()
        [sim.end_frame(self.args) for sim in self.simulators]
        # t_end = perf_counter()
        # print(f"\nPost Process +  time: {(t_end-t_start)*1000:.3f} ms ({t_end-t_start:f} s)")
        # print("")

    def update_computed_data(self):
        # Computation after simulation loop
        print("  --- Overwrite Object data ---")
        self.post_process.compute(self.args)

        # End simulators
        # End pre/post processing ?

        # Computation at the end of the simulation
        # A voir comment on peut faire ca et comment ca peut être utile
        # self.finalise_process.compute() #
        # Enfait ca seriait un geo node sur la simu cached
