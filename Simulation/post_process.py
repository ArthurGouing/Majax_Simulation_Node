from .graph import compute_order
from .operator import Operator
from Simulation.data.data_base import Data

class PostProcessing:
    # Operator data
    # ops:  dict[str, Operator]
    # Argument data
    # args: dict[str, Data] # datas c'est mieux ?
    # Ordered list of operator id_name in order to make the computation
    ordered_ops: list[Operator]
    # Information about the computation
    state: str

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
        ouputs: list[str] = ["BlExportGeoOperator"]
        self.ordered_ops = compute_order(ops, args, input_ops_name=inputs, output_ops_name=ouputs)
        self.ordered_ops = self.ordered_ops[1:]

    def compute(self, datas: dict[str, Data]) -> None:
        """Compute the pre processing operators"""
        print("Post Process")
        for op in self.ordered_ops: # cf class _iter__
            self.state = f"Computing {op.id_name}" + " | " # op.arg.inputs.get_memory
            # Retreve arguments
            input_args  = [datas[inp.data] for inp in op.inputs]
            output_args = [datas[out.data] for out in op.outputs]
            # print( "  Computing "+ op.id_name+" | Inputs arguments: ", *[arg.id_name for arg in input_args], sep=", ")

            # Execute the script
            op.compute(*input_args+output_args)