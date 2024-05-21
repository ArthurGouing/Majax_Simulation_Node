# Read data object from Blenderfile and convert them to Geometry data type
# Write solution Geometry to the selected Blender Object 

#### Library Import #### 
from time import perf_counter

#### Blender Import #### 
from bpy.types import Object, Node
from Simulation.data.data_base import Data

#### Local Import #### 
from .operator_base import Operator

class BlExportGeoOperator(Operator):
    def __init__(self, node: Node) -> None:
        super().__init__(node.name)
        self.prim_type = node.geo_options
        self.obj = node.obj

    def compute(self, *args: Data) -> None:
        t_start = perf_counter()
        # Update object points
        for i, p in enumerate(args[0].data.points):
            self.obj.data.vertices[i].co.x = p[0]
            self.obj.data.vertices[i].co.y = p[1]
            self.obj.data.vertices[i].co.z = p[2]
        t_end = perf_counter()
        print(f"\nWriting point time: {(t_end-t_start)*1000:.3f} ms ({t_end-t_start:f} s)")

        # Update object edges
        if self.prim_type=="Edge":
            t_start = perf_counter()
            for i, p in enumerate(args[0].primitives):
                self.obj.data.edges[i] = list(p)
            t_end = perf_counter()
            print(f"\nWriting point time: {(t_end-t_start)*1000:.3f} ms ({t_end-t_start:f} s)")
        
        # Update object faces
        elif self.prim_type=="Face":
            for i, p in enumerate(args[0].primitives):
                self.obj.data.polygons[i] = list(p)

        self.obj.data.update()
        return