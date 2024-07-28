#############################################################
# Copyright (C) 2025 Arthur Gouinguenet - All Rights Reserved
# This file is part of Majax Simulation Node project which is
# delivered under GNU General Public Liscense.
# For any questions or requests related to the use of this work
# please contact me directly at arthur.gouinguenet@free.fr
#############################################################

#### Local Import #### 
from .graph import Orderer
from .operator import Operator
from Simulation.data.data_base import Data

class PostProcessing:
    def __init__(self) -> None:
        """Init pre processing computer manager"""
        self.state = "Initialisation"
        self.ordered_ops = list()

    def order(self, ops: dict[str, Operator], args: dict[str, Data]) -> None:
        """Change the inputs and operators according to the graphs. rebuild or change"""
        self.state = "Updating graph"
        # from .operator import * 
        # BlSimOutputOperator
        inputs: list[str] = ["BlSimOutputOperator"]
        outputs: list[str] = ["BlExportGeoOperator"]

        order = Orderer(ops, args, inputs, outputs)
        self.ordered_ops = order.ordered_ops.copy()

        if order.sim_out in self.ordered_ops:
            self.ordered_ops.remove(order.sim_out)

        del order

    def compute(self, datas: dict[str, Data]) -> None:
        """Compute the pre processing operators"""
        for op in self.ordered_ops: # cf class _iter__
            self.state = f"Computing {op.id_name}" + " | " # op.arg.inputs.get_memory
            # Retreve arguments
            input_args  = [datas[inp.data] for inp in op.inputs]
            output_args = [datas[out.data] for out in op.outputs]
            # print( "  Computing "+ op.id_name+" | Inputs arguments: ", *[arg.id_name for arg in input_args], sep=", ")

            # Execute the script
            all_args = input_args + output_args
            unic_all_args = dict(zip(all_args, [""]*len(all_args))) # Kind of ordered set to avoid double data
            op.compute(*unic_all_args.keys()) 