# Computation grapmh: interface pour manipuler mes graphs avec mon compute_manager
# simulator: Simulator# can totally be inside the operators, with a compute functions
#from ..Blender_ui import SimulationNodeTree
# Add current dir to pythonpath
from bpy.types import NodeLink, Node
# from Blender_ui import SimulationNodeTree as bl_tree
from Simulation.data.data_base import Data
from Simulation.operator import Operator, __dict__

def compute_order(ops: dict[str, Operator], args: dict[str, Data], options: str=None, input_ops_name: list[str]=None, output_ops_name: list[str]=None) -> list[Operator]:
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
    # output_ops: list[Operator] = [op for op in self.operators if op.__class__.__name__ in output_ops_name]
    output_ops: list[Operator] = [op for op in ops.values() if op.__class__.__name__ in output_ops_name]
    # output_ops: list[Operator] = [op for op in ops if ]
    # input_args: list[Data] = sum([[inp for inp in output_op.inputs] for output_op in output_ops], [])
    # input_args: list[Data] = [inp for output_op in output_ops for inp in output_op.inputs]
    # Liste des Data que l'l'operator prend en input
    for op in output_ops:
        for inp in op.inputs:
            input_data = args[inp] # input_data = self.get_data(inp)
            find_available_input(ops, args, input_data, ordered_op, input_ops_name)
        ordered_op.append(op)
    return ordered_op

def find_available_input( ops: dict[str, Operator], args: dict[str, Data], arg: Data, ordered_op: list[Operator], stop_op: list[str]=None) -> None:
    op_name = arg.from_operator
    op = ops[op_name]
    # If the operator has already been execute, the input argument is available
    if op in ordered_op: # useless
        return
    # End of the dependency chain
    if not op.inputs: # End of the dependency chain
        ordered_op.append(op)
        for out in op.outputs: 
            output_data = args[out] # output_data = self.get_data(out)
            output_data.computable = True
    # Loop on inputs of the precedent operator
    else: 
        for inp in op.inputs:
            input_data = args[inp] # input_data = self.get_data(inp)
            # inp: str
            if  op.__class__.__name__ not in stop_op and not input_data.computable:
                find_available_input(ops, args, input_data, ordered_op, stop_op)
            input_data.computable = False # same as checking op  in ordered_op
        ordered_op.append(op)

# def get_data(self, data_name: str) -> Data:
#     for d in self.arguments:
#         if d.id_name==data_name:
#             return d
#     return None
# def get_op(self, op_name: str) -> Operator:
#     for o in self.operators:
#         if o.id_name==op_name:
#             return o
#     return None
        





