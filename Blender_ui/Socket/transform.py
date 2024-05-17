#### Import Library ####
#### Import Blender Library ####
from bpy.types import Context, UILayout, Node
#### Import files ####
from bpy.props import FloatVectorProperty
from .base_socket import MajaxSocketBase


class MajaxSocketTransform(MajaxSocketBase):
    """Vector socket type"""
    bl_idname = "MajaxSocketTransform"
    bl_label = "Transform"


    value: FloatVectorProperty(name="Value", description="Value x, y, z of the vector")

    def draw(self, context: Context, layout: UILayout, node: Node, text: str):
        layout.label(text=text)

    # Socket color
    @classmethod
    def draw_color_simple(cls):
        # Rose
        return (0.647, 0.329, 0.777, 1.0) # Gamma correcition == screen_color^0.45
