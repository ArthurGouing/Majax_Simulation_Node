# Read data object from Blenderfile and convert them to Geometry data type

#### Library Import #### 
import numpy as np

#### Blender Import #### 
import bpy
from bpy.types import Object, Node

#### Local Import #### 
from .operator_base import Operator
from Simulation.data.data_base import Data
from Simulation.data.geometry import Point, Prim, Geometry


class BlImportGeoOperator(Operator):
    def __init__(self, node: Node) -> None:
        super().__init__(node.name)
        self.prim_type = node.geo_options
        self.obj = node.obj
        self.use_double = node.double


    def compute(self, *args: Data) -> None:
        # Init
        points = list()
        prims = list()

        # Build points
        for v in self.obj.data.vertices:
            points.append([v.co.x, v.co.y, v.co.z, 1.0])

        # Build primitives : Edge case
        if self.prim_type=="EDGE":
            for p in self.obj.data.edges:
                prims.append(list(p.vertices))

        # Build primitives : Face case
        elif self.prim_type=="FACE":
            for p in self.obj.data.polygons:
                prims.append(list(p.vertices))

        # TODO: add option for read thetrahedreon primitives

        # Store Geometry
        dtype = np.double if self.use_double else np.single
        args[0].data = Geometry(points, prims, dtype)
