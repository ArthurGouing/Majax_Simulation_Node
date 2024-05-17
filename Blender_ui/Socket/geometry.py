#### Import Library ####
#### Import Blender Library ####
from bpy.types import Context, UILayout, Node
from bpy.types import NodeSocketGeometry
#### Import files ####
from bpy.props import StringProperty, BoolProperty, IntProperty
from .base_socket import MajaxSocketBase


class MajaxSocketGeometry(MajaxSocketBase):
    """Geometry CPU socket type"""
    bl_idname = "MajaxSocketGeometry"
    bl_label = "Geometry"

    size_expr: StringProperty(name="size_expr", description="python expression which return an tuple (or int) for the size of the buffer. Can use the inputs args data to create the size of the new buffer")

    def draw(self, context: Context, layout: UILayout, node: Node, text: str):
        layout.label(text=text)

    # Socket color
    @classmethod
    def draw_color_simple(cls):
        # Green
        return (0.0, 0.836, 0.636, 1.0)
