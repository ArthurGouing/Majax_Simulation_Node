#############################################################
# Copyright (C) 2025 Arthur Gouinguenet - All Rights Reserved
# This file is part of Majax Simulation Node project which is
# delivered under GNU General Public Liscense.
# For any questions or requests related to the use of this work
# please contact me directly at arthur.gouinguenet@free.fr
#############################################################


#### Library Import ####
from mathutils import Color

#### Import Blender ####
from bpy.types import Node

#### Import Intern File ####
from .base_node import BaseNode
from bpy.props import IntProperty


class IntegerParameterNode(BaseNode, Node):
    '''Create an Integer parameter'''
    # Optional identifier string.
    bl_idname = 'IntegerParameterNode'
    # Label for nice name display
    bl_label = "Parameter Integer"
    # Executor name
    operator = "BlCreateIntegerOperator"

    # === Properties ===
    value: IntProperty(name="Value", default=0)

    def init(self, context):
        # Set name and color
        self.name = self.bl_label.replace(" ", "_")
        self.use_custom_color = True
        self.color = Color((0.188, 0.163, 0.055))

        # Outputs
        self.outputs.new("MajaxSocketInteger", "Integer")
        self.outputs[-1].intent = "out"

    # Update Node when a link is modified or a node is added/deleted
    def update(self):
        pass

    # Properterties edition on the node.
    def draw_buttons(self, context, layout):
        layout.prop(self, "value")

    # Properties interface on the sidebar.
    def draw_buttons_ext(self, context, layout):
        layout.prop(self.outputs[0], "name")
        layout.prop(self, "value")