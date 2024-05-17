# Export bpy.obj.data types to the Initial object for viewing the result in the viewport
# Import the selected object as a Geometry type
from bpy.types import Node, Object
from bpy.props import PointerProperty, BoolProperty, EnumProperty

from .base_node import BaseNode

enum_prim = [
    ("NONE", "None", "Store only the points of the object for the computation", 1),
    ("EDGE", "Edge", "Store edge of the object into the primitives of the geometry for the computation", 2),
    ("FACE", "Face", "Store face of the object into the primitives of the geometry for the computation", 3),
]

class ExportGeoNode(BaseNode, Node):
    '''Execute the choosen script Kernel'''
    # Optional identifier string.
    bl_idname = 'ExportGeoNode'
    # Label for nice name display
    bl_label = "Export Geometry"
    # Operator name id
    operator = "BlExportGeoOperator"

    # === Properties ===
    obj: PointerProperty(type=Object, name="Target")
    geo_options: EnumProperty(items=enum_prim, name="Options")

    def init(self, context):
        self.name = self.bl_label.replace(" ", "_")
        self.inputs.new("MajaxSocketGeometry", "Geometry")
        self.inputs[-1].intent = "in"

    def update(self):
        """Rename unconnected inputs (i.e. no data associated with)"""
        for inp in self.inputs:
            if not inp.is_linked:
                inp.name = inp.bl_label # = "Geometry"

    # Properterties edition on the node.
    def draw_buttons(self, context, layout):
        layout.prop(self, "obj")
        layout.prop(self, "geo_options")

    # Properties interface on the sidebar.
    def draw_buttons_ext(self, context, layout):
        layout.prop(self, "obj")
        layout.prop(self, "geo_options")