import sys
import numpy as np
from abc import ABC
from bpy.types import NodeLink, Object, NodeSocket


from .geometry import Geometry
# from Simulation import Operator # for typing hint


DataType = Geometry | Object # | float | int | bool | Vector | Rotation | Transformation

class Data(ABC):
    # ==== Principal Data ====
    id_name: str
    # Data type
    data_type: str # Choose between ["Object", "Geometry", "GPU Buffer(s)", "float", "int", "Vector", "Rotation", "Tranform"]
    # static member count
    id: dict[str, int] = dict() # on le veut propre au datatype
    # Data that will be used by the script
    data: DataType
    #  Operator id_name which use this argument as an output
    from_operator: str = "none"
    # Operator which use this argument as an input

    # ==== Conveniant variable ====
    # To know which Argument contain usefull data
    computed: bool = False
    computable: bool = False 


    def __init__(self, socket: NodeSocket, from_op_name: str) -> None:
        # Get data type
        self.data_type: str = socket.bl_idname[10:] # Extract **** from NodeSocket<****> to get type
        # Update data_id
        self.id_name: str = self.data_type + "_" + from_op_name # where from_op_name is the node name
        # Save From operator id
        self.from_operator: str = from_op_name
        # Stock op id which create this data 
        self.data: DataType = None

        # Init other usefull variable
        self.computable: bool = False
        self.computed: bool = False
        return
        # Import data
        if self.from_operator.is_importer: # and precompute_import:
            self.data = self.from_operator.compute()
            self.is_None = False
        else:
            self.data = None

    def add_from_op(self, id_name: str) -> None:
        self.from_operator = id_name
    
    def load(self, new_data) -> None:
        self.data = new_data

    def used(self) -> None:
        self.computed = True

    def find_from_op(self, ops: list):
        for op in ops:
            if op.name==self.from_operator:
                return op

    def get_mem_size(self, format: str=None) -> str:
        """ Retrun the momery use of this argument"""
        if isinstance(self.data, np.ndarray):
            mem = self.data.nbytes
        else:
            mem = sys.getsizeof(self.data)

        if format=="KB":   return f"{mem/1000:.3f} KB"
        elif format=="MB": return f"{mem/1000000:.3f} MB"
        elif format=="GB": return f"{mem/1000000000:.3f} GB"
        else: print(f"Error the format {format} doesn't exist.")
        return ""

    def clean(self) -> None:
        """ Clean the data but keep the link in the computation graph"""
        if self.computed:
            self.data = None
            self.is_None = True