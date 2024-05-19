#### Import Blender ####
from bpy.types import Node
#### Import Intern File ####
from .base_node import BaseNode
from bpy.props import StringProperty, FloatProperty 



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

    def update(self):
        print("update float parameter node")
        pass

    # Properterties edition on the node.
    def draw_buttons(self, context, layout):
        layout.prop(self, "value")

    # Properties interface on the sidebar.
    def draw_buttons_ext(self, context, layout):
        layout.prop(self.outputs[0], "name")
        layout.prop(self, "value")