# Computation grapmh: interface pour manipuler mes graphs avec mon compute_manager
# simulator: Simulator# can totally be inside the operators, with a compute functions
#from ..Blender_ui import SimulationNodeTree
# Add current dir to pythonpath
from bpy.types import NodeLink, Node
# from Blender_ui import SimulationNodeTree as bl_tree
from Simulation.data.data_base import Data
from Simulation.operator import Operator, __dict__

op_class_list = [cl for n, cl in __dict__.items() if n[-8:]=="Operator"]


class ComputationGraph:
    """
    The computation graph store the data of the graph only.
    The manipulated argument don't store any data. 
    This class find the best operation order for doing the computation
    according to different criteria: 
    - Optimize memory usage (TODO)
    - Maximize parallel task i.e. Minimize waiting barrier (TODO)
    - ...
    """
    # Operator or the verticies of the graph
    operators: list[Operator] = list()
    # Datas or the links of the graph
    arguments: set[Data]     = set()    # data names ou dictionnaire au lieu de set, fonctionne pour l'init

    def __init__(self, bl_links: NodeLink, bl_nodes: Node) -> None:
        """Read the Blender graph"""
        # for link in bl_links:
        #     self.arguments.add(Data(link))
        self.operators = list()
        self.arguments = set()
        for node in bl_nodes:
            if node.type=='FRAME':
                continue
            for op_class in op_class_list:
                if op_class.__name__==node.operator:
                    # Initialize Operator
                    operator = op_class(node)
                    self.operators.append(operator)
                    break
            # Create Data slot for each output of the operator
            for socket in node.outputs:
                if socket.bl_idname=="NodeSocketVirtual" :
                    continue
                from_op_idname = operator.id_name
                argument = Data(socket, from_op_idname)
                self.arguments.update({argument}) # ca va pas marcher, les Data seront différent à cause des membre static ...
                # Store argument output of the operator
                operator.add_output(argument.id_name)

        # Link the data to the inputs of each operator
        for link in bl_links:
            # ReFind the data name
            input_data_name = link.from_socket.bl_idname[10:] + "_" + link.from_node.name
            # argument_name_list = [arg.id_name for arg in self.arguments]
            # Find the operator to link with
            output_op_name = link.to_node.name
            operator = self.get_op(output_op_name)
            operator.add_input(input_data_name)

    def get_ops(self) -> dict[str, Operator]:
        ops: dict[str, Operator] = dict()
        for op in self.operators:
            ops.update({op.id_name: op})
        return ops
    def get_args(self) -> dict[str, Data]:
        args: dict[str, Data] = dict()
        for arg in self.arguments:
            args.update({arg.id_name: arg})
        return args

    def compute_order(self, options: str=None, input_ops_name: list[str]=None, output_ops_name: list[str]=None) -> list[Operator]:
        """
        Return the ordered operators ready for computations
        Args:
            option: methode used to build the op_order. choose between ["..."]
            input_op: list of operator type to stop searching
            output_op: list of operator type to start the searching
        (because the orderer_op is build from the output)
        """
        # output_ops: list[ABCOperator] = [op for op in self.operator if op.bl_idname[6:]=="Export"] # put in post_process class
        ordered_op: list[Operator] = list()
        output_ops: list[Operator] = [op for op in self.operators if op.__class__.__name__ in output_ops_name]
        # input_args: list[Data] = sum([[inp for inp in output_op.inputs] for output_op in output_ops], [])
        # input_args: list[Data] = [inp for output_op in output_ops for inp in output_op.inputs]
        # Liste des Data que l'l'operator prend en input
        for op in output_ops:
            for inp in op.inputs:
                input_data = self.get_data(inp)
                self.find_available_input(input_data, ordered_op, input_ops_name)
            ordered_op.append(op)
        return ordered_op

    def find_available_input(self, arg: Data, ordered_op: list[Operator], stop_op: list[str]=None) -> None:
        op_name = arg.from_operator
        op = self.get_op(op_name)
        # If the operator has already been execute, the input argument is available
        if op in ordered_op:
            return
        # End of the dependency chain
        if not op.inputs: # End of the dependency chain
            ordered_op.append(op)
            for out in op.outputs: 
                output_data = self.get_data(out)
                output_data.computable = True
        # Loop on inputs of the precedent operator
        else: 
            for inp in op.inputs:
                input_data = self.get_data(inp)
                # inp: str
                if  op.__class__.__name__ not in stop_op and not input_data.computable:
                    self.find_available_input(input_data, ordered_op, stop_op)
                input_data.computable = False # same as checking op  in ordered_op
            ordered_op.append(op)
    
    def get_data(self, data_name: str) -> Data:
        for d in self.arguments:
            if d.id_name==data_name:
                return d
        return None
    def get_op(self, op_name: str) -> Operator:
        for o in self.operators:
            if o.id_name==op_name:
                return o
        return None
        





