#############################################################
# Copyright (C) 2025 Arthur Gouinguenet - All Rights Reserved
# This file is part of Majax Simulation Node project which is
# delivered under GNU General Public Liscense.
# For any questions or requests related to the use of this work
# please contact me directly at arthur.gouinguenet@free.fr
#############################################################


#### Library Import ####
from mathutils import Color

#### Blender Import ####
from bpy.types import Node, Object
from bpy.props import PointerProperty, EnumProperty

#### Intern File Import ####
from .base_node import BaseNode

# Enum Items
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
        # Set name and color
        self.name = self.bl_label.replace(" ", "_")
        self.use_custom_color = True
        self.color = Color((0.188, 0.163, 0.055))

        # Inputs
        self.inputs.new("MajaxSocketGeometry", "Geometry")
        self.inputs[-1].intent = "in"

    # Update Node when a link is modified or a node is added/deleted
    def update(self):
        """Rename unconnected inputs (i.e. no data associated with)"""
        for inp in self.inputs:
            if not inp.is_linked:
                inp.name = inp.bl_label  # = "Geometry"

    # Properterties edition on the node.
    def draw_buttons(self, context, layout):
        layout.prop(self, "obj")
        layout.prop(self, "geo_options")

    # Properties interface on the sidebar.
    def draw_buttons_ext(self, context, layout):
        layout.prop(self, "obj")
        layout.prop(self, "geo_options")
    