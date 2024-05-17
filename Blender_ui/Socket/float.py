#### Import Library ####
#### Import Blender Library ####
from bpy.types import Context, UILayout, Node
#### Import files ####
from .base_socket import MajaxSocketBase


class MajaxSocketFloat(MajaxSocketBase):
    """Float socket type"""
    bl_idname = "MajaxSocketFloat"
    bl_label = "Float"

    # === Properties ===

    def draw(self, context: Context, layout: UILayout, node: Node, text: str):
            layout.label(text=text)

    # Socket color
    @classmethod
    def draw_color_simple(cls):
        # Gray
        return (0.636, 0.636, 0.636, 1.0)
