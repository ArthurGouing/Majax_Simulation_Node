#### Import Library ####
#### Import Blender Library ####
from bpy.types import Context, UILayout, Node
#### Import files ####
from .base_socket import MajaxSocketBase

class MajaxSocketVector(MajaxSocketBase):
    """Vector socket type"""
    bl_idname = "MajaxSocketVector"
    bl_label = "Vector"

    def draw(self, context: Context, layout: UILayout, node: Node, text: str):
        layout.label(text=text)

    # Socket color
    @classmethod
    def draw_color_simple(cls):
        # Violet
        return (0.392, 0.392, 0.777, 1.0) # Gamma correcition == screen_color^0.45
