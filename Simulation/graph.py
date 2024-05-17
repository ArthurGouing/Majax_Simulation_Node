# Computation grapmh: interface pour manipuler mes graphs avec mon compute_manager
# simulator: Simulator# can totally be inside the operators, with a compute functions
#from ..Blender_ui import SimulationNodeTree
# Add current dir to pythonpath
from bpy.types import NodeLink, Node
# from Blender_ui import SimulationNodeTree as bl_tree
from Simulation.data.data_base import Data, Argument
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
    # Init
    ordered_op: list[Operator] = list()
    # Output operator, where we start walking on the graph
    output_ops: list[Operator] = [op for op in ops.values() if op.__class__.__name__ in output_ops_name]
    # Liste des Data que l'l'operator prend en input
    for op in output_ops:
        if not op.inputs:
            continue
        for inp in op.inputs:
            find_available_input(ops, args, inp, ordered_op, input_ops_name)
        ordered_op.append(op)
    return ordered_op

def find_available_input( ops: dict[str, Operator], datas: dict[str, Data], arg: Argument, ordered_op: list[Operator], stop_op: list[str]=None) -> bool:
    """
    Correct name should be find/fill argument dependency
    i.e. add all the op that need to be computed before to create the argument 'arg'
    """
    op_name = arg.from_op
    op = ops[op_name]
    # If the operator has already been execute, the input argument is available
    # if op in ordered_op: # useless
    #     return
    # End of the dependency chain
    if not op.inputs: # End of the dependency chain
        if op not in ordered_op:
            ordered_op.append(op)
        for out in op.outputs: 
            # output_data = args[out] # output_data = self.get_data(out)
            # output_data.computable = True
            datas[out.data].computable = True
    # Loop on inputs of the precedent operator
    else: 
        for inp in op.inputs:
            if  op.__class__.__name__ not in stop_op and not datas[inp.data].computable:
                find_available_input(ops, datas, inp, ordered_op, stop_op)
            datas[inp.data].computable = False # same as checking op  in ordered_op
        if op not in ordered_op:
            ordered_op.append(op)
        





