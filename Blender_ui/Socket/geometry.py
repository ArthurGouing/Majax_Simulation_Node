#### Import Library ####
#### Import Blender Library ####
from bpy.types import Context, UILayout, Node
from bpy.types import NodeSocketGeometry
#### Import files ####
from bpy.props import StringProperty, BoolProperty


class MajaxSocketGeometry(NodeSocketGeometry):
    """Geometry CPU socket type"""
    bl_idname = "MajaxSocketGeometry"
    bl_label = "Geometry"

    intent: StringProperty(name="intent", description="type of the socket", default="inout")  # TODO: delete (cf data/argument build)
    inout: BoolProperty(name="is_intent", description="bool which is true if socket type is inout.", default=True)
    size_expr: StringProperty(name="size_expr", description="python expression which return an tuple (or int) for the size of the buffer. Can use the inputs args data to create the size of the new buffer")

    def draw(self, context: Context, layout: UILayout, node: Node, text: str):
        layout.label(text=text)

    # Socket color
    @classmethod
    def draw_color_simple(cls):
        # Green
        return (0.0, 0.836, 0.636, 1.0)
