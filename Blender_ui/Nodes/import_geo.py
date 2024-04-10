# Import the selected object as a Geometry type
from bpy.types import Node, Object
from bpy.props import PointerProperty, BoolProperty, EnumProperty

from .base_node import BaseNode

enum_prim = [
    ("BOTH", "Both", "Store edge and face of the object into the primitives of the geometry for the computation", 3),
    ("EDGE", "Edge", "Store edge of the object into the primitives of the geometry for the computation", 1),
    ("FACE", "Face", "Store face of the object into the primitives of the geometry for the computation", 2),
    ("NONE", "None", "Store only the points of the object for the computation", 4),
]

def obj_name_update(self, context):
    if self.obj is not None:
        self.outputs[0].name = self.obj.name

class ImportGeoNode(BaseNode, Node):
    '''Execute the choosen script Kernel'''
    # Optional identifier string.
    bl_idname = 'ImportGeoNode'
    # Label for nice name display
    bl_label = "Import Geometry"
    # Executor name
    operator = "BlImportGeoOperator"

    # === Properties ===
    obj: PointerProperty(type=Object, name="Source", update=obj_name_update)
    geo_options: EnumProperty(items=enum_prim, name="Options")

    def init(self, context):
        self.name = self.bl_label.replace(" ", "_")
        self.outputs.new("NodeSocketGeometry", "Geometry")

    # def update(self):
    #     """Delete Unconnected virtual socket"""
    #     self.outputs[0].name = self.obj.name

    # Properterties edition on the node.
    def draw_buttons(self, context, layout):
        layout.prop(self, "obj")
        layout.prop(self, "geo_options")

    # Properties interface on the sidebar.
    def draw_buttons_ext(self, context, layout):
        layout.prop(self, "obj")
        layout.prop(self, "geo_options")