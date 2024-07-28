#################################################
# Copyright (C) 2025 Arthur Gouinguenet - All Rights Reserved
# This file is part of Majax Simulation Node project which is
# delivered under GNU General Public Liscense.
# For any questions or requests related to the use of this work
# please contact me directly at arthur.gouinguenet@free.fr
#############################################################

#### Local Import #### 
from Simulation.data.data_base import Data, Argument
from Simulation.operator import Operator, __dict__

class Orderer:
    def __init__(self, ops: dict[str, Operator], datas: dict[str, Data], input_ops_name: list[str]=None, output_ops_name: list[str]=None) -> None:
        # Initi varuable
        self.ops = ops
        self.datas = datas
        self.end_operators   = [op for op in ops.values() if op.__class__.__name__ in output_ops_name]
        self.start_operators = [op for op in ops.values() if op.__class__.__name__ in input_ops_name] 

        self.ordered_ops = list()
        self.sim_in  = None
        self.sim_out = None

        for op in self.end_operators:
            self.find_required_op(op)
        self.ordered_ops.reverse()

    def find_required_op(self, op: Operator) -> None:
        """ Add to oredered_ops, all the operator that need to be computed before computing op"""
        # Add operator 
        if op not in self.ordered_ops:
            self.ordered_ops.append(op)

        # track sim_in/sim_out operator
        if op.__class__.__name__=="BlSimInputOperator":
            self.sim_in=op
        elif op.__class__.__name__=="BlSimOutputOperator":
            self.sim_out=op

        # End condition
        if op in self.start_operators:
            return

        # Recursive find required ops
        for inp in op.inputs:
            inp_op = self.ops[inp.from_op]
            self.find_required_op(inp_op)
        if not op.inputs and op not in self.start_operators:
            print(f"Error: {op.id_name}, is not in start_operator and don't have input. Nothing happened in find_required_op function")

    def find_kernels(self, path_list: list[list[Operator]]) -> set[Operator]:
        # Tourver tous les paths
        paths = [[]]
        for op in self.end_operators:
            self.find_paths(op, paths, 0)
        print("all path: ")
        for p in paths:
            print([o.id_name for o in p], end=" | ")
        print("")

        # Garder les paths d'Operator qui vivent exclusivement sur GPU
        paths = [p for p in paths if p[-1]==self.sim_in]
                
        print("ker path", [o.id_name for o in sum(paths, [])])

        # faire un set des kernels du simulator + simin/simout
        kernels = set()
        for op in sum(paths, []):
            kernels.add(op)
        print("all kernel", [o.id_name for o in kernels])

        return kernels

    def find_paths(self, op: Operator, paths: list[list[Operator]], path_id: int) -> None:
        # Add op to paths
        paths[path_id].append(op)

        # End recursive chaine condition
        if op == self.sim_in:
            return

        # Recursive on all inputs argument operators
        is_first=True
        actual_path = paths[path_id].copy()
        for inp in op.inputs:
            inp_op = self.ops[inp.from_op]
            # Compute the next pahts
            if  is_first:
                self.find_paths(inp_op, paths, path_id)
                is_first=False
            # Create a new path
            else:
                paths.append(actual_path.copy())
                self.find_paths(inp_op, paths, len(paths)-1)