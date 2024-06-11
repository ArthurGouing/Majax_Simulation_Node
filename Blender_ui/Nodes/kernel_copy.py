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
from bpy.types import Node
from bpy.props import EnumProperty, StringProperty, BoolProperty

#### Intern File Import ####
from .base_node import BaseNode

# Enum item
buffer_type = [
    ('POINT', "Points", "Copy only the buffer which contain the points data", 0),
    ('PRIM', "Primitives", "Copy only the buffer which contain the primitives data", 1),
    ('POINT_VAR', "Point variable", "Copy the buffer point variable specify the name of the variable below", 2),
    ('PRIM_VAR', "Primitives variable", "Copy the buffer prim variable specify the name of the variable below ", 3),
    ('GROUP', "Group", "Copy the buffer which containt the group data", 4)
]



class KernelCopyNode(BaseNode, Node):
    '''Copy the value of the source buffers to the destination buffer'''
    # Optional identifier string.
    bl_idname = 'KernelCopyNode'
    # Label for nice name display
    bl_label = "Kernel Copy"
    # Operator reference that is associate with the node
    operator = "BlKernelCopyOperator"

    # === Properties ===
    buffer: EnumProperty(items=buffer_type, name="Buffer")
    var_name: StringProperty(name="Var name")
    wait: BoolProperty(name="Wait", default=False)
    from_point: BoolProperty(name="From points", default=False)

    def init(self, context):
        # Set name and color
        self.name = self.bl_label.replace(" ", "_")
        self.use_custom_color = True
        self.color = Color((0.059, 0.082, 0.188))

        # Inputs
        self.inputs.new('MajaxSocketBuffers', "Destination")
        self.inputs[-1].intent = "inout"
        self.inputs.new("MajaxSocketBuffers", "Source")
        self.inputs[-1].intent = "in"

        # Outputs
        self.outputs.new('MajaxSocketBuffers', "Destination")
        self.outputs[-1].intent = "inout"

    # Update Node when a link is modified or a node is added/deleted
    def update(self):
        pass

    # Properterties edition on the node.
    def draw_buttons(self, context, layout):
        layout.prop(self, "buffer")
        if self.buffer not in ['POINT', 'PRIM']:
            layout.prop(self, "var_name")
        row = layout.row()
        row.prop(self, "wait")
        row.prop(self, "from_point")

    # Properties interface on the sidebar.
    def draw_buttons_ext(self, context, layout):
        layout.prop(self, "buffer")
        if self.buffer not in ['POINT', 'PRIM']:
            layout.prop(self, "var_name")
        row = layout.row()
        row.prop(self, "wait")
        row.prop(self, "from_point")