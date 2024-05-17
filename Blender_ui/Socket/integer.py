#### Import Library ####
#### Import Blender Library ####
from bpy.types import Context, UILayout, Node
#### Import files ####
from .base_socket import MajaxSocketBase


class MajaxSocketInteger(MajaxSocketBase):
    """Integer socket type"""
    bl_idname = "MajaxSocketInteger"
    bl_label = "Integer"


    def draw(self, context: Context, layout: UILayout, node: Node, text: str):
        layout.label(text=text)

    # Socket color
    @classmethod
    def draw_color_simple(cls):
        # Gray
        return (0.317, 0.474, 0.324, 1.0)
