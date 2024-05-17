#### Import Blender ####
from bpy.types import Node
from bpy.props import FloatVectorProperty, BoolProperty
#### Import Intern File ####
from .base_node import BaseNode


class VectorParameterNode(BaseNode, Node):
    '''Create a vector parameter'''
    # Optional identifier string.
    bl_idname = 'VectorParameterNode'
    # Label for nice name display
    bl_label = "Parameter Vector"
    # Executor name
    operator = "BlCreateVectorOperator"

    # === Properties ===
    value: FloatVectorProperty(name="Param", description="Value x, y, z of the vector", default=(0, 0, 0), subtype='XYZ')
    v_type: BoolProperty(name="Point", default=1, description="to determine the 4th composante of the vector. If it's a point, w=1, v_type=1. If it's a vector, w=0, v_type=0")


    def init(self, context):
        self.name = self.bl_label.replace(" ", "_")
        self.outputs.new("MajaxSocketVector", "Vector")
        self.outputs[-1].intent = "out"

    def update(self):
        pass

    # Properterties edition on the node.
    def draw_buttons(self, context, layout):
        layout.prop(self, "v_type", text="Point(On) / Vector(Off)")
        col = layout.column()
        col.prop(self,'value',text = 'Values')

    # Properties interface on the sidebar.
    def draw_buttons_ext(self, context, layout):
        layout.prop(self.outputs[0], "name")
        layout.prop(self, "v_type", text="Point(On) / Vector(Off)")
        col = layout.column()
        col.prop(self,'value',text = 'Values')