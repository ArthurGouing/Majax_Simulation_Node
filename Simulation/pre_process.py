from .simulator import Simulator
from .graph import compute_order
from .operator import Operator, BlSimInputOperator
from Simulation.data.data_base import Data

class PreProcessing:
    # Ordered list of operator id_name in order to make the computation
    ordered_ops: list[Operator]
    # Information about the computation
    state: str

    def __init__(self) -> None:
        """Init pre processing computer manager"""
        self.state = "Initialisation"
        self.ops  = dict()
        self.args = dict()

    def order(self, ops: dict[str, Operator], args: dict[str, Data]) -> None:
        """Change the inputs and operators according to the graphs. rebuild or change"""
        self.state = "Updating graph"
        inputs: list[str] = ["BlImportGeoOperator"]
                            # + ["CreateBufferNode"]
        ouputs: list[str] = ["BlSimInputOperator"]
        self.ordered_ops = compute_order(ops, args, input_ops_name=inputs, output_ops_name=ouputs)
        self.ordered_ops = self.ordered_ops[:-1]

    def compute(self, datas: dict[str, Data]) -> None:
        """Compute the pre processing operators"""
        print("Pre Process")
        for op in self.ordered_ops: # cf class _iter__
            self.state = f"Computing {op.id_name}" + " | " # op.arg.inputs.get_memory
            # Retreive Arguments
            input_args = [datas[inp.data] for inp in op.inputs]
            output_args = [datas[out.data]  for out in op.outputs]
            # print( "  "+self.state+"Arguments: ", *[arg.id_name for arg in (input_args+output_args)], sep=", ")

            # Execute the script
            op.compute(*(input_args+output_args))