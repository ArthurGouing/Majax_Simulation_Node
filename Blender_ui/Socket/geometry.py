#### Import Library ####
#### Import Blender Library ####
from bpy.types import Context, UILayout, Node
from bpy.types import NodeSocketGeometry
#### Import files ####
from bpy.props import StringProperty

class MajaxSocketGeometry(NodeSocketGeometry):
    """Geometry CPU socket type"""
    bl_idname = "MajaxSocketGeometry"
    bl_label = "Geometry"

    intent: StringProperty(name="intent", description="type of the socket")

    def draw(self, context: Context, layout: UILayout, node: Node, text: str):
        layout.label(text=text)

    # Socket color
    @classmethod
    def draw_color_simple(cls):
        # Green
        return (0.0, 0.836, 0.636, 1.0)
