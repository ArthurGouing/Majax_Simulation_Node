#### Import Library ####
#### Import Blender Library ####
from bpy.types import Context, UILayout, Node
from bpy.types import NodeSocketVector
#### Import files ####
from bpy.props import StringProperty

class MajaxSocketVector(NodeSocketVector):
    """Vector socket type"""
    bl_idname = "MajaxSocketVector"
    bl_label = "Vector"

    intent: StringProperty(name="intent", description="type of the socket")

    def draw(self, context: Context, layout: UILayout, node: Node, text: str):
        layout.label(text=text)

    # Socket color
    @classmethod
    def draw_color_simple(cls):
        # Violet
        return (0.636, 0.636, 0.636, 1.0)
