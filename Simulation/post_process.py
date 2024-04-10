from .graph import ComputationGraph
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

    def update_graph(self, new_graph: ComputationGraph, ops: dict[str, Operator]) -> None:
        """Change the inputs and operators according to the graphs. rebuild or change"""
        self.state = "Updating graph"
        # from .operator import * 
        # BlSimOutputOperator
        inputs: list[str] = ["BlSimOutputOperator"]
        ouputs: list[str] = ["BlExportGeoOperator"]
        self.ordered_ops = new_graph.compute_order(input_ops_name=inputs, output_ops_name=ouputs)

    def compute(self, args: dict[str, Data]) -> None:
        """Compute the pre processing operators"""
        print("")
        print("Post Process:")
        for op in self.ordered_ops: # cf class _iter__
            self.state = f"Computing {op.id_name}" + " | " # op.arg.inputs.get_memory
            # Retreve arguments
            input_args = [args[input_id] for input_id in op.inputs]

            # Execute the script
            op.compute(*input_args)