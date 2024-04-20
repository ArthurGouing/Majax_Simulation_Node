#### Import Library ####
#### Import Blender Library ####
from bpy.types import Context, UILayout, Node
from bpy.types import NodeSocket
#### Import files ####
from bpy.props import StringProperty

# Custom socket type
class MajaxSocketBuffers(NodeSocket):
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

    intent: StringProperty(name="intent", description="type of the socket")
    point_size: StringProperty(name="point_size", description="Python expression to determine the size of the bufer, for the points channel")
    prim_size: StringProperty(name="prim_size", description="Pythobn expression to determine the size of the buffer, for the primitives channel")

    # Optional function for drawing the socket input value
    def draw(self, context: Context, layout: UILayout, node: Node, text: str):
        layout.label(text=text)

    # Socket color
    @classmethod
    def draw_color_simple(cls):
        # Blue
        return (0.0, 0.117, 0.672, 1.0)

# Customizable interface properties to generate a socket from.
# class NodeTreeInterfaceSocketBuffers(NodeTreeInterfaceSocket):
#     # The type of socket that is generated.
#     bl_socket_idname = "GeometryBuffersType"
# 
#     def draw(self, context, layout):
#         # Display properties of the interface.
#         layout.label("Test")
# 
#     # Set properties of newly created sockets
#     def init_socket(self, node, socket, data_path):
#         print("ini_socket")
#         # socket.input_value = self.default_value
#         # self.intent: str= "" # "in" or "out" or "inout"
#         pass
# 
#     # Use an existing socket to initialize the group interface
#     def from_socket(self, node, socket):
#         # Current value of the socket becomes the default
#         print("from socket")
#         # self.default_value = socket.input_value
#         pass