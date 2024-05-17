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
        self.name = self.bl_label.replace(" ", "_")
        self.outputs.new("MajaxSocketInteger", "Integer")
        self.outputs[-1].intent = "out"

    def update(self):
        pass

    # Properterties edition on the node.
    def draw_buttons(self, context, layout):
        layout.prop(self, "value")

    # Properties interface on the sidebar.
    def draw_buttons_ext(self, context, layout):
        layout.prop(self.outputs[0], "name")
        layout.prop(self, "value")