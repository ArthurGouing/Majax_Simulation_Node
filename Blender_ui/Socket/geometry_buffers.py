#### Import Library ####
#### Import Blender Library ####
from bpy.types import Context, UILayout, Node
#### Import files ####
from bpy.props import StringProperty
from .base_socket import MajaxSocketBase

# Custom socket type
class MajaxSocketBuffers(MajaxSocketBase):
    # Description string
    """Geometry GPU buffer socket type"""
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = "MajaxSocketBuffers"
    # Label for nice name display
    bl_label = "Geometry Buffers"
    # Can handl multiple inputs
    # display_shape = 'DIAMOND_DOT'
    # display_shape = 'DIAMOND'
    # display_shape = 'SQUARE_DOT'
    display_shape = 'SQUARE'

    expr_size: StringProperty(name="Size", description="Python expression to determine the size of the bufer", default="point size")

    # Optional function for drawing the socket input value
    def draw(self, context: Context, layout: UILayout, node: Node, text: str):
        layout.label(text=text)

    # Socket color
    @classmethod
    def draw_color_simple(cls):
        # Blue
        return (0.0, 0.117, 0.672, 1.0)