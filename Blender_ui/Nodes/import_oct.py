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
from bpy.props import PointerProperty, StringProperty, EnumProperty, BoolProperty

#### Intern File Import ####
from .base_node import BaseNode

# Enum item
enum_prim = [
    ("NONE", "None", "Store only the points of the object for the computation", 1),
    ("EDGE", "Edge", "Store edge of the object into the primitives of the geometry for the computation", 2),
    ("FACE", "Face", "Store face of the object into the primitives of the geometry for the computation", 3),
]

# Update functions
def geo_name_update(self, context):
    self.outputs[0].name = self.geo_name
def obj_name_update(self, context):
    if self.obj is not None:
        self.geo_name = self.obj.name



class ImportOctNode(BaseNode, Node):
    '''Load the geometry in an Octree'''
    # Optional identifier string.
    bl_idname = 'ImportOctNode'
    # Label for nice name display
    bl_label = "Import Octree"
    # Executor name
    operator = "BlImportOctOperator"

    # === Properties ===
    obj: PointerProperty(type=Object, name="Source", update=obj_name_update)
    geo_options: EnumProperty(items=enum_prim, name="Options")
    geo_name: StringProperty(name="Geometry name", description="Name of the geometry created from object (by default, the name of the object)", default="Geometry", update=geo_name_update)
    double: BoolProperty(name="Use double", description="Use double precision float for computation", default=False)

    def init(self, context):
        # Set name and color
        self.name = self.bl_label.replace(" ", "_")
        self.use_custom_color = True
        self.color = Color((0.188, 0.163, 0.055))

        # Outputs
        self.outputs.new("MajaxSocketGeometry", "Geometry")
        self.outputs[-1].intent = "out"

    # Update Node when a link is modified or a node is added/deleted
    def update(self):
        pass

    # Properterties edition on the node.
    def draw_buttons(self, context, layout):
        layout.prop(self, "obj")
        layout.prop(self, "geo_options")
        row = layout.row()
        row.prop(self, "double")

    # Properties interface on the sidebar.
    def draw_buttons_ext(self, context, layout):
        layout.prop(self, "obj")
        layout.prop(self, "geo_options")
        row = layout.row()
        row.prop(self, "double")
        layout.separator()
        layout.prop(self, "geo_name")