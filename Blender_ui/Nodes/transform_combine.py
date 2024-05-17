#### Import Blender ####
from bpy.types import Node
from bpy.props import FloatVectorProperty, BoolProperty
#### Import Intern File ####
from .base_node import BaseNode


class TransformCombineNode(BaseNode, Node):
    '''Create a vector parameter'''
    # Optional identifier string.
    bl_idname = 'TransformCombineNode'
    # Label for nice name display
    bl_label = "Combine Transform"
    # Executor name
    operator = "BlParameterTransform"

    # === Properties ===
    value: FloatVectorProperty(name="Param", size= 16, description="Value of the transformation matrix, ordered in raw-major (C like)")
    major_type: BoolProperty(name="Type", default=1, description="Determine if the Matrix is raw-major or column-major storage")
    # Add a parameter name properti ?

    def init(self, context):
        self.name = self.bl_label.replace(" ", "_")
        self.inputs.new("MajaxSocketVector", "Translation")
        self.inputs[-1].intent = "in"
        self.inputs.new("MajaxSocketFloat", "Rotation")
        self.inputs[-1].intent = "in"
        self.inputs.new("MajaxSocketVector", "Scale")
        self.inputs[-1].intent = "in"
        self.outputs.new("MajaxSocketTransform", "Transform")
        self.outputs[-1].intent = "out"

    def update(self):
        pass

    # Properterties edition on the node.
    def draw_buttons(self, context, layout):
        layout.prop(self, "major_type", text="Raw-Major(On) / Column-Major(Off)")

    # Properties interface on the sidebar.
    def draw_buttons_ext(self, context, layout):
        layout.prop(self.outputs[0], "name")
        layout.prop(self, "major_type", text="Raw-Major(On) / Column-Major(Off)")
        # TODO: add layout to see/modify the transfor 4x4 matrix