#############################################################
# Copyright (C) 2025 Arthur Gouinguenet - All Rights Reserved
# This file is part of Majax Simulation Node project which is
# delivered under GNU General Public Liscense.
# For any questions or requests related to the use of this work
# please contact me directly at arthur.gouinguenet@free.fr
#############################################################


#### Import Blender ####
from bpy.types import Node
from bpy.props import FloatProperty 

#### Import Intern File ####
from .base_node import BaseNode



class FloatParameterNode(BaseNode, Node):
    '''Create a float parameter'''
    # Optional identifier string.
    bl_idname = 'FloatParameterNode'
    # Label for nice name display
    bl_label = "Parameter Float"
    # Executor name
    operator = "BlCreateFloatOperator"

    # === Properties ===
    value: FloatProperty(name="Value", default=0)

    def init(self, context):
        self.name = self.bl_label.replace(" ", "_")
        self.outputs.new("MajaxSocketFloat", "Float")
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